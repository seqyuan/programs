"""
For KEGG Classification, outfile is sample_KEGG_Classification.pdf

In file format:
    Group   Classification  Value
    Cell growth and death   A   109
    Transport and catabolism    A   167
    Cell motility   A   32
    ...
    ...

Date 20170718
"""
import argparse
import os
import sys
import re
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
Bin = os.path.abspath(os.path.dirname(__file__))

__author__='Yuan Zan'
__mail__= 'seqyuan@gmail.com'
__date__= '20170718'

class kegg_class:
    df = None
    legend_df = None
    ax = None
    maxvalue = None
    N = None

    def Init(self,class_file,ax,sample,outdir):
        df = pd.read_table(class_file, header = 0, index_col=None, encoding='utf-8')
        df =df[::-1]
        df.reset_index(inplace=True,drop = True)

        df['color'] = None
        colors = ['#464451','#DAD9DE','#F0E6DD','#E0BCC8','#A986A7','#3A4340','#4C6371']
        colors2 = ['#C82FC8','#3952A4','#E22C90','#35B449','#42297A','#D54672','#E5D86F']
        colors3 = ['#DD82E1','#FFA1C6','#8973E0','#00B2F2','#4473C5','#FFC102','#BBD3C6']
        colors4 = ["brown","teal","coral","dodgerblue","peru","goldenrod","b","g","r","c","m","y"]       
        colors.extend(colors2)
        colors.extend(colors3)
        colors.extend(colors4)

        df_copy = df.copy()
        ii = -1
        classi = None
        for i,r in df_copy.iterrows():
            if classi != r['Classification']:
                ii += 1
                classi = r['Classification']
            df.ix[i,'color'] = colors[ii]

        df['classNum'] = 1
        df2 = df[['Classification','classNum','color']]

        self.ax = ax
        self.maxvalue = df['Value'].describe()['max']
        self.df = df
        self.legend_df = df2.groupby(['Classification','color'], axis=0).sum()[::-1]
        self.N = self.df.shape[0]

    def plot_barth(self):
        self.ax.barh(bottom=range(self.N),width=self.df['Value'],height=0.8,left=0,color=self.df['color'],edgecolor=self.df['color'],align='center',alpha=1)
        for i,row in self.df.iterrows():
            self.ax.text(row['Value'] + self.maxvalue*0.01, i, row['Value'], ha='left', va= 'center',fontsize=7)

        self.ax.set_yticks([i for i in range(self.N)])
        self.ax.set_yticklabels(self.df['Group'],rotation='horizontal',fontsize='smaller')
        self.ax.set_xlabel('Number of Genes')
        self.ax.tick_params(bottom ='on',top='off',left='off',right='off')

    def plot_legend(self):
        bottom = 0
        for i,r in self.legend_df.iterrows():
            self.ax.bar(left=[self.maxvalue*1.12], height=[r['classNum']-0.3], width=4, bottom=bottom-0.345,color=i[1],align="edge",edgecolor=i[1])
            self.ax.text(self.maxvalue*1.16, bottom + (r['classNum'])/2, i[0], ha='left', va= 'center',fontsize=10)
            bottom += r['classNum']
        self.ax.set_xlim([0,self.maxvalue*1.2])
        self.ax.set_ylim([-1,self.N+1])

def main():
    parser=argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='author:\t{0}\nmail:\t{1}\ndate:\t{2}\n'.format(__author__,__mail__,__date__))
    parser.add_argument('-c','--classFile',help='class.txt',dest='classi',type=str,required=True)
    parser.add_argument('-s','--sample',help='sample',type=str,default='sample')
    parser.add_argument('-o','--outDir',help='outDir',dest='outDir',type=str,default=Bin)

    args=parser.parse_args()

    fig = plt.figure(figsize=(8,8))
    [ax_x, ax_y, ax_w, ax_h] = [0.35,0.1,0.6,0.8]   #[0.05,0.07,0.07,0.66] 
    ax = fig.add_axes([ax_x, ax_y, ax_w, ax_h], frame_on=True, axisbg = 'white')

    kc = kegg_class()
    kc.Init(args.classi,ax,args.sample,args.outDir)
    kc.plot_barth()
    kc.plot_legend()

    ax.axhline(-1, color='k',linewidth=3)
    ax.set_title('KEGG Classification')
#    ax.set_xlim([0,])
    fig.savefig(os.path.join(args.outDir,"{0}_KEGG_Classification.pdf".format(args.sample)))
    fig.savefig(os.path.join(args.outDir,"{0}_KEGG_Classification.png".format(args.sample)))

if __name__=="__main__": 
    main()
