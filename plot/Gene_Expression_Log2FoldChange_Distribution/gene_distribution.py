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


files = os.path.join(Bin,"case_control.anno.txt")
chr_file = os.path.join(Bin,"chrom_mm9.sizes")


df = pd.read_table(files,header = 0,index_col=None,encoding='utf-8')
chr_size = pd.read_table(chr_file,header = None,index_col=None,names=['chr','size'],encoding='utf-8')


df = df[df['Significant'] == "yes"]
df = df[['Log2FoldChange','Up/Down','Position']]
#df.to_csv("case_control.anno.txt",sep='\t',columns=None, header=True)

fig = plt.figure(figsize=(12,8))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], frame_on=True, axisbg = 'white')

for i,r in chr_size.iterrows():
    ax.plot([0,r['size']],[i+5,i+5],linestyle='-', color='k', linewidth=1,label=r['chr'],gid=r['chr'])

ax.set_yticks([i+5 for i in chr_size.index])
ax.set_yticklabels(chr_size['chr'],rotation='horizontal',fontsize='x-large')
ax.set_xlabel("Along chromosome")
ax.tick_params(bottom ='on',top='off',left='off',right='off')

chr_size['pose'] = chr_size.index +5
chr_size.index = chr_size['chr']

df=df.replace([np.inf, -np.inf], 0)
describe = df['Log2FoldChange'].describe()


for i,r in df.iterrows():
    pos = re.split(":|-", r['Position'])
    if pos[0] not in chr_size['chr']:
        continue

    colors = ['r','b']
    color = ""
    w = int(pos[2]) - int(pos[1])
    left=[pos[1]]
    height= []
    if r['Log2FoldChange'] >0:
        height = [r['Log2FoldChange']/describe['max']/1.3]
    elif r['Log2FoldChange'] <0:
        height = [-r['Log2FoldChange']/describe['min']/1.3]
    else:
        continue

    if height[0] >0:
        color = colors[0]
    else:
        color = colors[1]
    width=[w]
    bottom=[chr_size.ix[pos[0],'pose']]
    ax.bar(left=left, height=height, width=width, bottom=bottom,color=color,align="edge",edgecolor=color)


plt.title("Gene Expression Log2FoldChange Distribution")

fig.savefig(os.path.join(Bin,"Gene_Expression_Log2FoldChange_Distribution.pdf"))
