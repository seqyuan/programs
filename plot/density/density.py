'''
	对每一列的值取log2，然后做density曲线
'''
#!/usr/bin/env python3
# coding: utf-8 -*-
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import pandas as pd
import numpy as np
__author__='Yuan Zan'
__mail__= 'seqyuan@gmail.com'

def usage():
	sys.stderr.write('{0}\n\tAuthor:\t{1}\n\tEmail:\t{2}\n'.format(__doc__,__author__,__mail__))
	sys.stderr.write("\n\tusage:\n\t\tpython3 {0} infile outfile title xlabel\n".format(__file__))
	sys.stderr.write("\n\texample:\n\t\tpython3 {0} fpkm.xls fpkm.boxplot.pdf \'Distribution of Sample Expression\' \'log2FPKM\'\n".format(__file__))
	sys.stderr.write("\n\texample:\n\t\tpython3 {0} fpkm.xls fpkm.boxplot.png \'Distribution of Sample Expression\' \'log2FPKM\'\n".format(__file__))
	sys.exit(1)

def prettify(ax,x_max):
	ax.set_xlim(left=-10,right=x_max)
	ax.set_ylim(bottom=-0.005)

	aa = ['bottom','left','right','top']
	for i in aa:
		ax.spines[i].set_color('black')
		ax.spines[i].set_linewidth(1)
	ax.tick_params(bottom ='on',top='off',left='on',right='off')
	legend = ax.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.,prop={'size':8},ncol=2)
	legend.get_frame().set_facecolor('white')

def main(args):
	infile,outfile,title,xlabel = args

	fig = plt.figure(figsize=(8, 6))
	[ax_x, ax_y, ax_w, ax_h] = [0.15,0.1,0.5,0.8]
	ax = fig.add_axes([ax_x, ax_y, ax_w, ax_h], frame_on=True, axisbg = 'white')

###-------------导入数据------------
	df = pd.read_table(infile,header=0,index_col = 0, encoding='utf-8')
	df = np.log2(df+0.0000001)
	x_max = max(df.describe().ix['max'])
#	df = pd.concat([df,df],axis=1)
###-------------画图------------
	goodcolors = ['#004DA1','#F7CA18','#4ECDC4','#F9690E','#B35AA5','#7DCDF3','#0080CC','#F29F41','#DE6298','#C4EFF6','#C8F7C5','#FCECBB','#F9B7B2','#E7C3FC','#81CFE0','#BDC3C7','#EDC0D3','#E5EF64','#4ECDC4','#168D7C','#103652','#D2484C','#E79D01']
	cnames =  goodcolors + sorted(list(matplotlib.colors.cnames.keys()))[::2][::-1]

	df.plot(kind='density',ax=ax,color = cnames)
	ax.set_xlabel(xlabel)
	ax.set_title(title)

	prettify(ax,x_max)

	plt.savefig(outfile)

if __name__ == '__main__':
	if len(sys.argv) != 5:
		usage()
	main(sys.argv[1:])
