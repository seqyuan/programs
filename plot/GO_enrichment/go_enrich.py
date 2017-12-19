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

#import warnings
#warnings.filterwarnings("ignore")

Bin = os.path.abspath(os.path.dirname(__file__))

__author__='Yuan Zan'
__mail__= 'seqyuan@gmail.com'
__date__= '20171219'

class up_down_go_enrich:
    df = None
    legend_df = None
    ax = None

    def Init(self,gene_up_down_enrich_go_file,ax,sample,outdir):
        df = pd.read_table(gene_up_down_enrich_go_file, header = 0, index_col=False, encoding='utf-8')
        self.df = df
        df['termcolor'] = '#CFE65A'
        df['ke'] = 0
        df.loc[df['GO Term']=='cellular_component','termcolor'] = '#FEF3C6'
        df.loc[df['GO Term']=='molecular_function','termcolor'] = '#87A26B'

        i = df[df['GO Term']=='biological_process'].index[0]        
        df.loc[i,'ke'] = 1
        ii = df[df['GO Term']=='cellular_component'].index[0]
        df.loc[ii,'ke'] = 1
        iii = df[df['GO Term']=='molecular_function'].index[0]
        df.loc[iii,'ke'] = 1

        self.df = df
        self.ax = ax      

    def plot_bar(self):
        bar_width = 0.3
        #rects3 = self.ax.bar(self.df.index, [100]*self.df.shape[0], 1, alpha=0.5, color=self.df['termcolor'], label=self.df['GO Term'],align='edge')
        for i,row in self.df.iterrows():
            if row['ke'] == 1:
                self.ax.bar([i], [100], 1, alpha=1, color=row['termcolor'],edgecolor=row['termcolor'],label=row['GO Term'],align='edge')
            else:
                self.ax.bar([i], [100], 1, alpha=1, color=row['termcolor'],edgecolor=row['termcolor'],align='edge')
        self.ax.legend()

        rects1 = self.ax.bar(self.df.index+0.2, self.df['Up_Percent']*100, bar_width, alpha=1, color='#951F2B', label='Up',align='edge')
        rects2 = self.ax.bar(self.df.index+0.2+bar_width, self.df['Down_Percent']*100, bar_width, alpha=1, color='#9ABBA6', label='Down',align='edge')
           
        for i in ['bottom','left','top','right']:
            self.ax.spines[i].set_color('black')
            self.ax.spines[i].set_linewidth(0.5)

        #self.ax.set_yticks([i for i in range(self.N)])
        self.ax.set_xticks(list(self.df.index+0.5))
        self.ax.set_xticklabels(list(self.df['GO Subterm']),rotation=70,fontsize='smaller',ha='right')
        self.ax.set_ylabel('Percent of Genes')
        self.ax.tick_params(bottom ='on',top='off',left='on',right='off')
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.set_xlim([0,self.df.shape[0]])
        self.ax.set_ylim([0,100])
        self.ax.grid(False)

        self.ax.legend()
        
        #xlabels = self.ax.get_xticklabels()
        #for xl in xlabels:
        #    xl.set_rotation(15)

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
    parser.add_argument('-f','--updown',help='D_G_Up_Down.txt file',dest='updown',type=str,required=True)
    parser.add_argument('-s','--sample',help='sample',type=str,default='sample')
    parser.add_argument('-o','--outDir',help='outDir',dest='outDir',type=str,default=Bin)

    args=parser.parse_args()

    fig = plt.figure(figsize=(9,7),facecolor='white')
    [ax_x, ax_y, ax_w, ax_h] = [0.1,0.6,0.8,0.35]   #[0.05,0.07,0.07,0.66] 
    ax = fig.add_axes([ax_x, ax_y, ax_w, ax_h], frame_on=True,axisbg = 'white')

    udge = up_down_go_enrich()
    udge.Init(args.updown,ax,args.sample,args.outDir)
    udge.plot_bar()
    #kc.plot_legend()

    ax.set_title(args.sample)
#    ax.set_xlim([0,])
    fig.savefig(os.path.join(args.outDir,"{0}_Up_Down.pdf".format(args.sample)),facecolor = fig.get_facecolor(),edgecolor ='none')
    fig.savefig(os.path.join(args.outDir,"{0}_Up_Down.png".format(args.sample)),facecolor = fig.get_facecolor(),edgecolor ='none')

if __name__=="__main__": 
    main()
