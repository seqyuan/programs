'''
Imports an tab-delimited expression matrix
export fpkm distribution box figure
'''
#!/usr/bin/env python3
# coding: utf-8 -*-
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')         #使画出的图为ggplot风格
import pandas as pd
###-------------定义图片对象------------
__author__='Yuan Zan'
__mail__= 'seqyuan@gmail.com'

def usage():
	sys.stderr.write('{0}\n\tAuthor:\t{1}\n\tEmail:\t{2}\n'.format(__doc__,__author__,__mail__))
	sys.stderr.write("\n\tusage:\n\t\tpython3 {0} infile outfile\n".format(__file__))
	sys.stderr.write("\n\texample:\n\t\tpython3 {0} fpkm.xls fpkm.boxplot.pdf\n".format(__file__))
	sys.exit(1)

def prettify(ax,box_plot,df):
	colors = [name for name, hex in matplotlib.colors.cnames.items()]
	for patch, color in zip(box_plot['boxes'], colors):
		patch.set_facecolor(color)

	ax.set_xticklabels(df.columns,rotation='vertical')
	ax.tick_params(bottom ='on',top='off',left='on',right='off') #去掉tick线
	aa = ['bottom','left','right','top']
	for i in aa:
		ax.spines[i].set_color('black')
		ax.spines[i].set_linewidth(1)
	ax.set_ylim([-0.5,30])
	ax.set_ylabel('FPKM Value')
	ax.set_title('FPKM Distribution')

def main(args):
	infile,outfile = args

	fig = plt.figure(figsize=(8, 8))
	ax = fig.add_subplot(111,axisbg='white')
###-------------导入数据------------
	df = pd.read_table(infile,header=0,index_col = 0, encoding='utf-8')
###-------------画图------------
	box_plot = ax.boxplot([df[i] for i in df.columns],showfliers=False,patch_artist=True)
	plt.setp(box_plot['whiskers'], color='black', lw=1)
	plt.setp(box_plot['medians'], color='black')
	plt.setp(box_plot['caps'], color='black', lw=1)	
	plt.setp(box_plot['boxes'], color='black')

	prettify(ax,box_plot,df)
	plt.savefig(outfile)

if __name__ == '__main__':
	if len(sys.argv) != 3:
		usage()
	main(sys.argv[1:])
