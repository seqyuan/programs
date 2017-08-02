"""
禅道bug状态提取程序,计算bug修复及时率
"""
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
#sys.setdefaultencoding('utf-8')
#sys.path.append("D:\\Program Files (x86)\\Anaconda3\\Lib\\site-packages")
import pandas as pd
import numpy as np
import pymysql as mdb
import datetime
import warnings
import configparser
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
plt.style.use('ggplot')


__author__='Yuan Zan'
__mail__= 'seqyuan@gmail.com'

class myconf(configparser.ConfigParser):
    def __init__(self,defaults=None):
        configparser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        return optionstr


def set_resolved_closed_bug_deadline(bug_df,cursor):
    #为已解决或已关闭的bug加一个deadline(日期为 解决/关闭 那一天+0.1d)
    finished_no_deadline_df = bug_df[((bug_df['status']=="closed") | (bug_df['status']=="resolved")) & pd.isnull(bug_df['deadline'])]
    
    for i,row in finished_no_deadline_df.iterrows():
        deadline = row['closedDate']
        if pd.isnull(deadline) or deadline== None:
            deadline = row['resolvedDate']

        deadline += datetime.timedelta(days=0.1)
        deadline = deadline.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE zt_bug SET deadline = %s WHERE id = %s",(deadline,row['id']))

def set_a_deadline_for_active(bug_df,cursor):
    #状态是active的bug加一个deadline(紧急度 1 = now+3d, 紧急度 2 = now+5d,紧急度 3 = now+15d)
    active_no_deadline_df = bug_df[(bug_df['status']=="active") & pd.isnull(bug_df['deadline'])]

    for i,row in active_no_deadline_df.iterrows():
        if row['status'] == "active" and pd.isnull(row['deadline']):
            deadline = datetime.datetime.now()
            if row['severity'] == 1:
                deadline += datetime.timedelta(days=3)
            elif row['severity'] == 2:
                deadline += datetime.timedelta(days=7)
            elif row['severity'] == 3:
                deadline += datetime.timedelta(days=14)
            else:
                deadline += datetime.timedelta(days=30)
            
            deadline = deadline.strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("UPDATE zt_bug SET deadline = %s WHERE id = %s",(deadline,row['id']))



def bug_statis(bug_df,start_time,end_time):
    time_not_null_df = bug_df[~pd.isnull(bug_df['deadline'])]
    in_time_df = time_not_null_df[(time_not_null_df['deadline'] >= start_time) & (time_not_null_df['deadline'] <= end_time)]  
    in_time_df['bug_num'] = 1
    in_time_df2 = in_time_df.copy()

    for i,row in in_time_df2.iterrows():
        if row['assignedTo'] == 'closed' or (~pd.isnull(row['resolvedBy'])):
            in_time_df.ix[i,'assignedTo'] = row['resolvedBy']

        if pd.isnull(row['closedDate']):
            in_time_df.ix[i,'closedDate'] = datetime.datetime.now().date()

        if pd.isnull(row['resolvedDate']):
            in_time_df.ix[i,'resolvedDate'] = datetime.datetime.now().date()

    #输入时间段内#每个人bug总数统计

    bug_sum_by_man_df = in_time_df.groupby('assignedTo').sum()['bug_num']
    #bug_sum_by_man_df_ = pd.DataFrame(bug_sum_by_man_df.tolist(),index=list(bug_sum_by_man_df.index),columns=['need'])


    #输入时间段内#每个人在截止日期前完成bug数统计
    in_time_df['resolvedDate'] = pd.to_datetime(in_time_df['resolvedDate']).apply(lambda x: x.date())
    in_time_df['closedDate'] = pd.to_datetime(in_time_df['closedDate']).apply(lambda x: x.date())

    finish_before_deadline_df = in_time_df[(in_time_df['resolvedDate']<=in_time_df['deadline']) | (in_time_df['closedDate']<=in_time_df['deadline'])]
    finish_before_deadline_df = finish_before_deadline_df.groupby('assignedTo').sum()['bug_num']
    #finish_before_deadline_df_ = pd.DataFrame(finish_before_deadline_df.tolist(),index=list(finish_before_deadline_df.index),columns=['finished'])

    df = pd.concat([bug_sum_by_man_df, finish_before_deadline_df],axis=1)
    df.columns = ['need','finished']
    df=df[df.index!=""]
    df = df.fillna(value=0)
    df['rate'] = df['finished']/df['need']

    return df

def plotall(df,config,start_time,end_time):
    groups = config.sections()

    axes1 = plt.subplot2grid((7,7),(0,0),rowspan=3,colspan=3,axisbg = 'white')
    axes2 = plt.subplot2grid((7,7),(4,0),rowspan=3,colspan=3,axisbg = 'white')
    axes3 = plt.subplot2grid((7,7),(0,4),rowspan=3,colspan=3,axisbg = 'white')
    axes4 = plt.subplot2grid((7,7),(4,4),rowspan=3,colspan=3,axisbg = 'white')
    axlist = [axes1,axes2,axes3,axes4]


    for i,group in enumerate(groups):
        member = config.options(group)
        plot_bar(axlist[i],df,group,member,config,start_time,end_time)     

def plot_bar(ax,df,title,names,config,start_time,end_time):
    ax2 = ax.twinx()
    ax2.grid(False)
    ax.grid(False)

    new_df = pd.DataFrame(index=names)
    new_df['need'] = 0
    new_df['finished'] = 0
    new_df['rate'] = 1

    for i,row in df.iterrows():
        if i in list(names):
            new_df.ix[i,:] = row

    new_df.index = [config.get(title,i) for i in new_df.index]
 
    ax.bar([ii + 0.2 for ii in range(new_df.shape[0])],new_df['need'],width=0.3,bottom=[0]*new_df.shape[0],label='应完成',color='#004DA1')
    ax.bar([ii + 0.5 for ii in range(new_df.shape[0])],new_df['finished'],width=0.3,bottom=[0]*new_df.shape[0],label='完成',color='#F7CA18')
    
    for i in range(new_df.shape[0]):
        ax.text(i+0.35, new_df.ix[i,'need']+0.05, '%.0f' % new_df.ix[i,'need'], ha='center', va= 'bottom')
        ax.text(i+0.65, new_df.ix[i,'finished']+0.05, '%.0f' % new_df.ix[i,'finished'], ha='center', va= 'bottom')

        ax2.text(i+0.5, new_df.ix[i,'rate']+0.01, '%.2f' % new_df.ix[i,'rate'], ha='center', va= 'bottom')
    
    ax.set_xticks(np.arange(0.5,new_df.shape[0]))
    ax.set_xticklabels(new_df.index,rotation='horizontal',fontsize='x-large')
    ax.set_ylim([0,max(new_df['need'])*1.5])
    legend = ax.legend(bbox_to_anchor=(1.07, 1), loc=2, borderaxespad=0.,prop={'size':8},ncol=1,fontsize=12)
    legend.get_frame().set_facecolor('white')
    ax.set_ylabel("Bug Number")
    ax.tick_params(bottom ='off',top='off',left='on',right='off')

    ax2.plot([ii + 0.5 for ii in range(new_df.shape[0])],new_df['rate'],linestyle='-',label='及时率',linewidth=2)  
    ax2.set_ylim([0,1.1])
    ax2.set_ylabel("bug修复及时率")
    ax.set_title('{0}\n{1} {2}'.format(title,start_time,end_time))
    ax2.tick_params(bottom ='off',top='off',left='off',right='on')

    legend2 = ax2.legend(bbox_to_anchor=(1.07, 0.85), loc=2, borderaxespad=0.,prop={'size':8},ncol=1,fontsize=12)
    legend2.get_frame().set_facecolor('white')
    aa = ['bottom','left','right','top']
    for i in aa:
        ax2.spines[i].set_color('black')
        ax2.spines[i].set_linewidth(1) 




def main():
    # 打开数据库连接
    config = {
        'host': '192.168.xx.xxx',
        'port': xxxx,
        'user': 'xxxx',
        'passwd': 'xxxx',
        'db': 'zentao',
        'charset': 'utf8'
    }

    conn = mdb.connect(**config)
    cursor = conn.cursor()
    config=myconf()
    #config(allow_no_value=True)
    config.readfp(open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'groups.ini'),encoding="utf-8"))


    try:
        bug_df = pd.read_sql('SELECT * FROM zt_bug', con=conn)[['id','severity','status','resolvedBy','assignedDate','deadline','resolvedDate','closedBy','closedDate','assignedTo']]
       
        #set_resolved_closed_bug_deadline(bug_df,cursor)   
   
        #set_a_deadline_for_active(bug_df,cursor)   
        start_time = datetime.datetime.strptime('2017-07-01','%Y-%m-%d').date()
        end_time = datetime.datetime.now().date()

        df = bug_statis(bug_df,start_time,end_time)
        
        fig = plt.figure(figsize=(14, 7))
        plotall(df,config,start_time,end_time)
      
        fig.savefig(os.path.join(os.getcwd(),"{0}_{1}_bug修复及时率.pdf".format(start_time,end_time)))
        plt.show()
 
    except:
        import traceback
        traceback.print_exc()
        # 发生错误时会滚
        conn.rollback()
    finally:
        # 关闭游标连接
        cursor.close()
        # 关闭数据库连接
        conn.close()

if __name__ == '__main__':
    #if len(sys.argv) != 5:
    #    usage()
    main()
