#!/usr/bin/env python
# coding: utf-8 -*- 

import pandas as pd
import numpy as np
import os
import sys
import re
import matplotlib
#matplotlib.use('Agg')
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


file = '/Users/yuanzan/Documents/programe_project/python/3D_plot/Transcriptome_samples_PCA3_analysis_groups.txt'
df = pd.read_csv(file,header=0, index_col = None, encoding='utf-8',sep="\t")

colors = ["brown","teal","coral","dodgerblue","peru","b","g","r","c","m","y"]
markers = ["v","o","^",",","p","H"]

class_1 = df.Group.unique()
df['Gcol'] = colors[0]
df['Mark'] = markers[0]


for i,v in enumerate(class_1):
    df.loc[df[df['Group']==v].index,'Gcol'] = colors[i]
    ii = 0
    for ioi in df[df['Group']==v].index:
        df.loc[ioi, 'Mark'] = markers[ii]
        ii += 1

fig = plt.figure(figsize=(6, 6))
[ax1_x, ax1_y, ax1_w, ax1_h] = [0.1,0.1,0.7,0.7]
ax = fig.add_axes([ax1_x, ax1_y, ax1_w, ax1_h], frame_on=True, facecolor = 'white',projection='3d')

for i,row in df.iterrows():   
    ax.scatter(row['PC1'], row['PC2'], row['PC3'], color=row['Gcol'], s=60, label=row['Group'], marker=row['Mark'])
ax.view_init(10, 150)

ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')

legend = ax.legend(loc=2,bbox_to_anchor=(1, 1), frameon=False, fontsize=11.5,ncol=1)
legend.get_frame().set_facecolor('white')

plt.show()

