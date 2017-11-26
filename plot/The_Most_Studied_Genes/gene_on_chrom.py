#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
usage:
    plot genes on chromosome
    python3 g.pene_on_chrom.py -i gene_info_total_human.tsv

Created on Sun Nov 11 23:23 2017
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
mpl.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import warnings
warnings.filterwarnings("ignore")
import argparse
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def plot_barth(ax, df, N):
    ax.barh(bottom=range(N),width=df['citations'],height=0.85,left=0,color='#00AEEF',edgecolor='#00AEEF',align='center',alpha=1)
    for i,row in df.iterrows():
        text = format(row['citations'],',')
        if i == 0:
            text = '{} citations'.format(text)
        ax.text(100, i, text, ha='left', va= 'center',fontsize=7,color='w')
   
    ax.set_xticks([])
    ax.set_yticklabels([])
    ax.tick_params(bottom ='off',top='off',left='off',right='off')
    ax.set_ylim([N+1,-1])

def plot_title(df,ax):
    t = 'THE TOP {}'.format(df.shape[0])
    tt = 'The {0} most studied genes of all time are described in more than {1} papers.'.format(df.shape[0],format(df['citations'].sum(),','))

    ax.text(0, 2, t, ha='left', va= 'center',fontsize=17,color='y',fontweight='bold')
    ax.text(0, 0, tt, ha='left', va= 'center',fontsize=8,color='#00AEEF')
    ax.set_ylim([-1,2])
    ax.tick_params(bottom ='off',top='off',left='off',right='off')
    ax.set_xticks([])
    ax.set_yticks([])

def plot_ylabel(df,ax):
    for i,row in df.iterrows():
        ax.text(0, i, '{0} {1}'.format(i+1,row['gene']), ha='left', va= 'center',fontsize=9,color='#00AEEF')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylim([df.shape[0]+1,-1])

def main(args):
    all_gene_counts_file, chromInfo, cytoBand = args

    df_gene_citation_counts = pd.read_table(all_gene_counts_file,header=None,index_col=None,names=['9606','un','id','chrom','start','end','name','describe','funcclass','citations'],encoding='utf-8')
    df_cytoband = pd.read_table(cytoBand,header=None,index_col=None,names=['chrom','start','end','p','c'],encoding='utf-8')
    df_chrominfo = pd.read_table(chromInfo,header=None,index_col=None,names=['chrom','length','s'],encoding='utf-8')

    df_cytoband = df_cytoband[df_cytoband['c'] == 'acen']

    
    df = df.sort_values(by=['citations'],ascending=False)
    df.index = list(range(df.shape[0]))
    df = df[['gene','describe','citations']].ix[0:args.topNum-1,:]

    h = 3
    if args.topNum > 10:
        h = int(args.topNum/10) * h

    fig = plt.figure(figsize=(6,h))

    [ax_x, ax_y, ax_w, ax_h] = [0.3,0.1,0.6,0.7]
    ax_barh = fig.add_axes([ax_x, ax_y, ax_w, ax_h], frame_on=False, axisbg = '#231F20')
    plot_barth(ax_barh, df, args.topNum)

    [ax1_x, ax1_y, ax1_w, ax1_h] = [0.1,0.1,0.2,0.7]
    ax1 = fig.add_axes([ax1_x, ax1_y, ax1_w, ax1_h], frame_on=False, axisbg = '#231F20')
    plot_ylabel(df, ax1)

    [ax2_x, ax2_y, ax2_w, ax2_h] = [0.1,0.8,0.7,0.1]
    ax2 = fig.add_axes([ax2_x, ax2_y, ax2_w, ax2_h], frame_on=False, axisbg = '#231F20')
    plot_title(df, ax2)

    #plt.show()
    fig.savefig(args.outfile)

if __name__ == '__main__':
    args = ['all_gene_counts.tsv','chromInfo.txt','cytoBand.txt']
    main(args)