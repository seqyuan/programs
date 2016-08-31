#!/usr/bin/env python3
#coding: utf-8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import utils, encoders
import mimetypes, sys,smtplib,socket,getopt
import os
Bin = os.path.abspath(os.path.dirname(__file__))
import time
import getpass
import configparser
import sqlite3
import argparse

__author__='ahworld'
__mail__= 'ahworld@yodagene.com'

class SendMail:
    def __init__(self,smtp_server,from_name,from_addr,to_addr,cc_addr,user,passwd):
        self.mailserver=smtp_server
        self.from_addr=from_addr
        self.to_addr=to_addr
        self.cc_addr=cc_addr
        self.username=user
        self.password=passwd
        self.from_name=from_name
    def attachment(self,filename):
        fd=open(filename,'rb')
        filename=filename.split('/')
        mimetype,mimeencoding=mimetypes.guess_type(filename[-1])        
        if (mimeencoding is None) or (mimetype is None):
            mimetype='application/octet-stream'       
        maintype,subtype=mimetype.split('/')
        if maintype=='text':
            retval=MIMEText(fd.read(), _subtype=subtype, _charset='utf-8')          
        else:
            retval=MIMEBase(maintype,subtype)
            retval.set_payload(fd.read())
            Encoders.encode_base64(retval)
            retval.add_header('Content-Disposition','attachment',filename=filename[-1])
            fd.close()
        return retval
    def msginfo(self,msg,subject,filename): 
        message=msg
        msg=MIMEMultipart()
        msg['To'] = self.to_addr
        msg['Cc'] = self.cc_addr
        msg['From'] = self.from_name + '<'+self.from_addr+'>'
        msg['Date'] = utils.formatdate(localtime=1)
        msg['Message-ID'] = utils.make_msgid()
        if subject:
            msg['Subject'] = subject
        if message:
            body=MIMEText(message,_subtype='plain')
            msg.attach(body)

        if filename:
            msg.attach(self.attachment(filename))
        return msg.as_string()
    def send(self,msg=None,subject=None,filename=None):
        try:
            s=smtplib.SMTP(self.mailserver)
            try:
                s.login(self.username,self.password)                
            except Exception as e:
                #print (e)
                print ("passworld is wrong")
                print ("Authentication failed:")
                sys.exit()
            to_addrs = self.to_addr + ';' + self.cc_addr
            s.sendmail(self.from_addr,to_addrs.split(';'),self.msginfo(msg,subject,filename))
        except Exception as e:
#            print (e)
            print ("passworld is wrong")
            print ("*** Your message may not have been sent!")
            sys.exit()
        else:
            print ("Message successfully sent to %d recipient(s)" %len(self.to_addr))

class myconf(configparser.ConfigParser):
    def __init__(self,defaults=None):
        configparser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        return optionstr

def clear(usrDin,diconf):
    if not usrDin.has_section('dinner'):
        usrDin.add_section("dinner")
    usrDin.remove_section('dinner')
    if not usrDin.has_section('usrNum'):
        usrDin.add_section("usrNum")
    usrDin.set('usrNum','num',str(0))
    if not usrDin.has_section('firstMan'):
        usrDin.add_section("firstMan")
    try:
        usrDin.remove_option('firstMan','mailMan')
    except:
        pass
    usrDin.write(open(diconf, "w"))

def select_usr(cur,user):
    select_sql = 'select * from dinnerusr where user = \'{0}\''.format(user)
    cur.execute(select_sql)
    theUser = cur.fetchall()
    if len(theUser) == 1:
        return (theUser[0])
    else:
        return ('usrNotExist')

def dinnerEmail(menu,cur,usrDin,week,Bin,mail,pwd):
    #pwd = getpass.getpass(prompt='please input your email password: ')
    mailTo = r'xingzheng@yodagene.com'
    copyTo = r'boss<boss@yodagene.com>;<leader1@yodagene.com>'
    #mailTo = r'zanyuan@yodagene.com'
    #copyTo = r'yfinddream@qq.com'
    msg = '您好！\n\n\t\t晚上需要加班，麻烦帮忙订餐，谢谢啦!\n'
    if not usrDin.has_section('dinner'):
        usrDin.add_section("dinner")
    arrnum = usrDin.options('dinner')
    if len(arrnum) > 0:
        for key in usrDin.items('dinner'):
            theUser = select_usr(cur,key[0])
            if theUser == 'usrNotExist': continue
            try:
                copyTo = copyTo + ';' + theUser[3]
                group = '分析组-RNA&表观组'
                if theUser[4]:
                    group = theUser[4]
                msg = msg + '\t\t科技服务事业部-生物信息部-' + group + '-' + theUser[2] + '-晚餐-' + menu.get(week,key[1]) + '\n'
            except Exception as e:
                print (e)
        try:
            subject = '订餐-科技服务事业部-生物信息部-晚餐' + str(len(arrnum)) + '份\n'
            mailman = usrDin.get('firstMan','mailMan')
            theUser = select_usr(cur,mailman)

            msg = msg + '\n祝好！\n' + theUser[2]
            mailMan = '生物信息部'
            if mail == theUser[3]:
                mailMan = theUser[2]
            test = SendMail('smtp.exmail.qq.com',mailMan,mail,mailTo,copyTo,mail,pwd)
        
            test.send(msg,subject,'')
            print ("Dinner email send successfully!")
        except Exception as e:
            print (e)
            print ("passworld is wrong\n")
            sys.exit()
    else:
        print ("今天没人订餐，就别发邮件了！")
 
def main():
    parser=argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='author:\t{0}\nmail:\t{1}'.format(__author__,__mail__))

    parser.add_argument('-db','--db',help='usr.db',dest='db',type=str,default='{0}/tmp/usr.db'.format(Bin))
    parser.add_argument('-ud','--usrDinner',help='usrDinner.ini',type=str,dest='usrDinner',default='{0}/usrDinner.ini'.format(Bin))
    parser.add_argument('-dm','--DinnerMenu',help='menu.ini',type=str,dest='DinnerMenu',default='{0}/menu.ini'.format(Bin))
    parser.add_argument('-m','--mail',help='email',dest='mail',type=str,default='seqyuan@yodagene.com')
    parser.add_argument('-pwd','--pwd',help='password',dest='pwd',type=str,required=True)    
    args=parser.parse_args()

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()
    usrDin=myconf()
    menu=myconf()

    usrDin.readfp(open(args.usrDinner))
    menu.readfp(open(args.DinnerMenu))
    week = time.strftime("%a")
    dinnerEmail(menu,cur,usrDin,week,Bin,args.mail,args.pwd)
    clear(usrDin,args.usrDinner)
    cur.close()
    conn.close()
if __name__ == '__main__':
    main()
