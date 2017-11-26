#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
usage:
    python3 ttt.py -i gene_info_total_human.tsv

Created on Sat Nov 11 21:26 2017
author: Zan Yuan
email: seqyuan@gmail.com
github: github.com/seqyuan
blog: www.seqyuan.com
WeChat Official Account: seqyuan
"""

import os
import sys
import pandas as pd
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import warnings
warnings.filterwarnings("ignore")
import argparse
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def str_len_format(text, format_len):
    text = text + (format_len - len(text) + 1) * '-'
    return text

def plot_barth(ax, df, N):
    ax.barh(bottom=range(N),width=df['citations'],height=0.8,left=0,color='#00AEEF',edgecolor='#00AEEF',align='center',alpha=1)
    max_text_len = 0
    for i,row in df.iterrows():
        text = row['citations']
        if i == 0:
            text = '{} citations'.format(text)
        ax.text(2, i, text, ha='left', va= 'center',fontsize=7,color='w')
        if len('{0} {1}'.format(i+1,row['gene'])) > max_text_len:
            max_text_len = len('{0} {1}'.format(i+1,row['gene']))
    
    ax.set_xticks([])
    ax.set_yticks([i for i in range(N)])
    ylabel = [str_len_format('{0} {1}'.format(i+1,row['gene']),max_text_len) for i,row in df.iterrows()]
    for i in ylabel:
        print (i)
    ax.set_yticklabels(ylabel,color='#00AEEF',horizontalalignment='left',verticalalignment='center')
    ax.tick_params(bottom ='off',top='off',left='off',right='off')
    ax.set_ylim([N+1,-1])

def main():
    parser=argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--gene_info', dest='gene_info', required=True, help='gene_info_total_human.tsv', type=str)
    parser.add_argument('-n', '--topNum', dest='topNum', default=10, help='top number to dispaly', type=int)
    parser.add_argument('-o', '--outfile', dest='outfile', default=os.path.join(os.path.abspath(os.path.dirname(__file__)),"The_top_citations.pdf"), help='out put pdf file')
    args=parser.parse_args()

    df = pd.read_table(args.gene_info,header=None,index_col=None,names=['9606','un','-','gene','describe','class','citations'],encoding='utf-8')
    df = df.sort_values(by=['citations'],ascending=False)
    df.index = list(range(df.shape[0]))
    df = df[['gene','describe','citations']].ix[0:args.topNum-1,:]

    fig = plt.figure(figsize=(6,8))
    [ax_x, ax_y, ax_w, ax_h] = [0.4,0.1,0.5,0.7]
    ax_barh = fig.add_axes([ax_x, ax_y, ax_w, ax_h], frame_on=False, axisbg = '#231F20')
    plot_barth(ax_barh, df, args.topNum)



    plt.show()

if __name__ == '__main__':
    main()