#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
usage:
    plot genes on chromosome
    python3 g.pene_on_chrom.py -i gene_info_total_human.tsv

Created on Sun Nov 12 23:23 2017
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
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

class chrom_class:
    df_chrominfo = None
    df_cytoband = None
    df_gene_citation_counts = None
    pad = 0

    def Init_read_file(self,chromInfo,cytoBand,all_gene_counts_file):
        df_gene_citation_counts = pd.read_table(all_gene_counts_file,header=None,index_col=None,names=['9606','un','id','chrom','start','end','name','describe','funcclass','citations'],encoding='utf-8')
        self.df_gene_citation_counts = df_gene_citation_counts.sort_values(by=['citations'],ascending=False)
        self.df_gene_citation_counts['Ranking'] = list(range(1,df_gene_citation_counts.shape[0] + 1))
        self.df_gene_citation_counts['citations'] = df_gene_citation_counts['citations']/df_gene_citation_counts['citations'].max()

        df_cytoband = pd.read_table(cytoBand,header=None,index_col=None,names=['chrom','start','end','p','c'],encoding='utf-8')
        self.df_chrominfo = pd.read_table(chromInfo,header=None,index_col=None,names=['chrom','length','s'],encoding='utf-8')
        self.df_chrominfo = self.df_chrominfo[::-1]
        self.df_chrominfo.index = list(range(self.df_chrominfo.shape[0]))
        self.df_cytoband = df_cytoband[df_cytoband['c'] == 'acen']
        self.pad = self.df_chrominfo['length'].max().max() * 0.02

    def plot_Rounded_Rectangle(self,ax):
        for i, row in self.df_chrominfo.iterrows():
            chr_cen = self.df_cytoband[self.df_cytoband['chrom'] ==row['chrom']][['start','end']]
            chr_cen_start = chr_cen.min().min()
            chr_cen_end = chr_cen.max().max()
            boxstyle = "round,pad={0}".format(self.pad)
            left_Rectangle = FancyBboxPatch((0+self.pad, (i*10+1)*self.pad), chr_cen_start - self.pad, self.pad * 7, boxstyle=boxstyle, facecolor='#313131', edgecolor='#313131')
            right_Rectangle = FancyBboxPatch((chr_cen_end + self.pad, (i*10+1)*self.pad), row['length'] - chr_cen_end, self.pad * 7, boxstyle=boxstyle, facecolor='#313131', edgecolor='#313131')
            cent_Rectangle = FancyBboxPatch((chr_cen_start + self.pad, (i*10+3)*self.pad), chr_cen_end - chr_cen_start, self.pad * 3, boxstyle="square,pad=0", facecolor='#313131', edgecolor='#313131')            
            ax.add_patch(left_Rectangle)
            ax.add_patch(right_Rectangle)
            ax.add_patch(cent_Rectangle)
            ax.text(0, (i*10+6)*self.pad, row['chrom'].lstrip('chr'), ha='left', va= 'center',fontsize=17,color='y',fontweight='bold')

            chrom_df = self.df_gene_citation_counts[self.df_gene_citation_counts['chrom'] == row['chrom']] 
            width = list(chrom_df['end'] - chrom_df['start'])
            bottom=[i*10*self.pad] * len(width)
            height=chrom_df['citations']*8.8*self.pad
            left=chrom_df['start'] + self.pad
            ax.bar(left=left, height=height, width=width, bottom=bottom,color='y',edgecolor='y',align='edge',alpha=1)
   
            if row['chrom'] in ['chrY','chr5']:
                ax.text(row['length'] + 3.4 * self.pad, i*10*self.pad, 'Number of studies\ndescribing each gene', ha='left', va= 'bottom',fontsize=17,color='w',fontweight='normal')

                xmin = row['length'] + 2.7 * self.pad
                xwidth = 0
                ymin = i*10*self.pad
                yhight = 7 * self.pad
                linewidth = 1 # axis line width
                head_width = self.pad
                head_length = self.pad
                overhang = self.pad * 0.5
                #ax.arrow(xmin, ymin, xwidth, yhight, fc='k', ec='k', linewidth = linewidth, head_width=head_width, head_length=head_length, overhang = overhang, length_includes_head = True, clip_on = False) 
                #ax.axhline(y=i*10*self.pad, xmin = row['length'] + 3.2 * self.pad, xmax=row['length'] + 3.6 * self.pad)

            elif row['chrom'] == 'chrX':
                chrx_most_citation_gene = chrom_df.sort_values(by=['Ranking']).iloc[0,:]
                ax.text(chrx_most_citation_gene['start'] + self.pad, i*10*self.pad + chrx_most_citation_gene['citations']*7.5*self.pad, chrx_most_citation_gene['name'], ha='left', va= 'bottom',fontsize=11,color='#899096',fontweight='normal')
            else:
                pass

        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.tick_params(bottom ='off',top='off',left='off',right='off')
        ax.set_xlim([0,self.df_chrominfo['length'].describe().max() + 2 * self.pad])
        ax.set_ylim([0,self.df_chrominfo.shape[0] * self.pad *10])

    def plot_top_10(self,ax):
        df = self.df_gene_citation_counts[self.df_gene_citation_counts['Ranking'] <= 10]
        for i, row in df.iterrows():
            iii = self.df_chrominfo[self.df_chrominfo['chrom']==row['chrom']].index[0] 
            ax.bar(left=row['start'] + self.pad, height=row['citations']*8.8*self.pad, width=row['end'] - row['start'], bottom=iii*10*self.pad,color='#00AEEF',edgecolor='#00AEEF',align='edge',alpha=1)
            x = row['start'] + self.pad
            y = iii*10*self.pad + row['citations']*7.5*self.pad
            ha = 'left'
            va= 'bottom'
            text = str(row['Ranking']) + ' ' + row['name']
            if row['Ranking'] == 1:
                va = 'top'
                y = iii*10*self.pad + row['citations']*8*self.pad
            elif row['Ranking'] == 8:
                x = row['start']
                y = iii*10*self.pad + row['citations']*8.8*self.pad
                ha = 'right'
            
            ax.text(x, y, text, ha=ha, va= va,fontsize=11,color='#00AEEF',fontweight='normal')

    def plot_title_arrow(self,ax):
        i = self.df_chrominfo.shape[0]
        xmin = 38 * self.pad
        ymin = i*10.2*self.pad
        xwidth = 2.6*self.pad
        yhight = 0
        linewidth = 1 # axis line width
        head_width = self.pad*2
        head_length = self.pad * 0.001
        overhang = self.pad * 0.5
        ax.arrow(xmin, ymin, xwidth, yhight, fc='k', ec='k', linewidth = linewidth, head_width=head_width, head_length=head_length, overhang = overhang, length_includes_head = True, clip_on = False) 
        #ax.axvline(x=xmin, ymin = 0, ymax=i*10*self.pad)

def plot_text(ax):
    text = """
In 2002, the US National Library of Medicine (NLM) began annotating papers in its
popular PubMed database of biomedical literature. Articles are tagged if they contain
information about the structure, function or location of a specific gene or gene product.
The effort has recorded 1.2 million descriptions of 27,000 human genes - including RNA
genes and pseudogenes - in about 565,000 articles. These data reveal trends in
genetics research, as well as the list of most studied human genes. 
    """
    ax.text(0, 0, text, ha='left', va= 'bottom',fontsize=16,color='w',fontweight='normal')
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_ylim([0,0.5])
    ax.set_ylim([0,0.85])
    ax.tick_params(bottom ='off',top='off',left='off',right='off')

def plot_title(ax):
    ax.text(0, 0, 'TOP GENES', ha='left', fontsize='40',color='y',fontweight='bold')
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.tick_params(bottom ='off',top='off',left='off',right='off')

def main(args):
    all_gene_counts_file, chromInfo, cytoBand = args
    fig = plt.figure(figsize=(11,17),facecolor='k')
    #fig.patch.set_facecolor('black')
    [ax_x, ax_y, ax_w, ax_h] = [0.05,0.03,0.9,0.8]
    ax_chrom = fig.add_axes([ax_x, ax_y, ax_w, ax_h], frame_on=False, axisbg = 'k')
    
    chrom = chrom_class()
    chrom.Init_read_file(chromInfo, cytoBand, all_gene_counts_file)
    chrom.plot_Rounded_Rectangle(ax_chrom)
    chrom.plot_top_10(ax_chrom)
    ax_chrom.set_title('Gene position on the chromosome',fontsize=16,color='w')
    #chrom.plot_title_arrow(ax_chrom)


    [ax_x1, ax_y1, ax_w1, ax_h1] = [0.05,0.85,0.9,0.08]
    ax_text = fig.add_axes([ax_x1, ax_y1, ax_w1, ax_h1], frame_on=False, axisbg = 'k')
    plot_text(ax_text)

    [ax_x2, ax_y2, ax_w2, ax_h2] = [0.05,0.97,0.9,0.03]
    ax_title = fig.add_axes([ax_x2, ax_y2, ax_w2, ax_h2], frame_on=False, axisbg = 'k')
    plot_title(ax_title)

    #plt.show()
    fig.savefig('gene_on_chrom.pdf',facecolor = fig.get_facecolor(),edgecolor ='none')
    fig.savefig('gene_on_chrom.png',facecolor = fig.get_facecolor(),edgecolor ='none')

if __name__ == '__main__':
    args = ['all_gene_counts.tsv','chromInfo.txt','cytoBand.txt']
    main(args)