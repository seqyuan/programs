#!/usr/bin/env python3
# coding: utf-8 -*- 
'''
Imports an tab-delimited expression matrix and produces and hierarchically clustered heatmap
sample cluster: method = euclidean, metric = average
gene cluster: method = euclidean, metric = complete
'''
import os
import sys
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
plt.style.use('ggplot')

import scipy
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as dist

import warnings
warnings.filterwarnings("ignore")
import time
import os

__author__='Yuan Zan'
__mail__= 'seqyuan@gmail.com'


def read_data(infile):
    df = pd.read_table(infile,header=0,index_col=0,encoding="utf-8")
    vmin = df.describe().ix['min'].min()
    vmax = df.describe().ix['max'].max()
    vmin_all = min([abs(vmax),abs(vmin)])
    if vmin_all != 0 and vmin < 0:
        df[df>vmin_all] = vmin_all
        df[df<-vmin_all] = -vmin_all
    return df

##-------------------------left dendrogram-------------------------------- 
def plot_ax1(df,fig,method,metric):
    [ax1_x, ax1_y, ax1_w, ax1_h] = [0.05,0.22,0.3,0.6]

    ax1 = fig.add_axes([ax1_x, ax1_y, ax1_w, ax1_h], frame_on=True, axisbg = 'white')

    d1 = dist.pdist(df)
    D1 = dist.squareform(d1)  # full matrix
    
    Y1 = sch.linkage(D1, method=method, metric=metric) 

    Z1 = sch.dendrogram(Y1, orientation='left')
    ind1 = sch.fcluster(Y1,0.7*max(Y1[:,2]),'distance') ### This is the default behavior of dendrogram
    ax1.set_xlim([df.shape[0],0])
    ax1.set_xticks([]) ### Hides ticks
    ax1.set_yticks([])

    return Z1,ind1

##-------------------------up dendrogram--------------------------------
def plot_ax2(df,fig,method,metric):
    [ax2_x, ax2_y, ax2_w, ax2_h] = [0.35,0.82, 0.5, 0.15] 
    ax2 = fig.add_axes([ax2_x, ax2_y, ax2_w, ax2_h], frame_on=True, axisbg = 'white')

    d2 = dist.pdist(df.T)
    D2 = dist.squareform(d2)
    Y2 = sch.linkage(D2, method=method, metric=metric) ### array-clustering metric - 'average', 'single', 'centroid', 'complete'
    Z2 = sch.dendrogram(Y2)
    ind2 = sch.fcluster(Y2,0.7*max(Y2[:,2]),'distance')
    ax2.set_xticks([]) ### Hides ticks
    ax2.set_yticks([])

    return Z2,ind2

##-------------------------heatmap--------------------------------
def plot_pcolormesh(df,Z1,Z2,fig):
    [axm_x, axm_y, axm_w, axm_h] = [0.35, 0.22, 0.5, 0.6]
    axm = fig.add_axes([axm_x, axm_y, axm_w, axm_h], axisbg = 'white')

    index_sort = Z1['leaves'] ### apply the clustering for the array-dendrograms to the actual matrix data
    columns_sort = Z2['leaves']
    df = df.iloc[index_sort,columns_sort]
    
    vmin = df.describe().ix['min'].min()
    vmax = df.describe().ix['max'].max() 
    norm = mpl.colors.Normalize(vmin/2, vmax/2) ### adjust the max and min to scale these colors
    colors = [mpl.cm.bwr,plt.cm.RdYlGn]
    cmap = colors[0]

    im = axm.pcolormesh(df, cmap=cmap, norm=norm)
    colorbar(axm,im,vmax,vmin) 

    axm.set_ylim([df.shape[0],0])
    axm.tick_params(bottom ='off',top='off',left='off',right='off') #去掉tick线
    axm.set_xticks([i+0.5 for i in range(df.shape[1])])
    axm.set_xticklabels(df.columns,rotation='vertical',fontsize='x-large')
    axm.set_yticks([])
    #axm.yaxis.tick_right()
    #axm.set_yticklabels(df.index,rotation='horizontal',fontsize='x-small')
    
    return df

def colorbar(axm,im,vmax,vmin):
    axins1 = inset_axes(axm, width="10%", height="10%", loc=2, bbox_to_anchor=(-0.3, 0.2, 2.5, 1.01), bbox_transform=axm.transAxes,) 
    cbar=plt.colorbar(im, cax=axins1, orientation='horizontal',ticks=[int(vmin/2), 0, int(vmax/2)])
    cbar.ax.set_title('Color Key',fontsize=15,y=1.02)

################# Perform the hierarchical clustering #################
def heatmap(df, fig):
    method = ['average', 'single', 'median', 'ward', 'weighted', 'centroid', 'complete']    ### gene-clustering metric - 
    metric= ['euclidean','cityblock','mahalanobis']
    
    Z1,ind1 = plot_ax1(df,fig,method[6], metric[0])
    Z2,ind2 = plot_ax2(df,fig,method[0], metric[0])
    df = plot_pcolormesh(df,Z1,Z2,fig)
#    plt.show()
    plt.savefig('heatmap.pdf')

def main(infile):
    df = read_data(infile)

    fig = plt.figure(figsize=(7,6))
    heatmap(df,fig)

def usage():
    sys.stderr.write('{0}\n\tAuthor:\t{1}\n\tEmail:\t{2}\n'.format(__doc__,__author__,__mail__))
    sys.stderr.write("\n\tusage:\n\t\tpython3 {0} rpkm.txt\n".format(__file__))
    sys.exit(1)
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        
    start_time = time.time()
    main(sys.argv[1])

    time_diff = str(round(time.time()-start_time,1))
    print ('Hierarchically clustering completed in {} seconds'.format(time_diff))

