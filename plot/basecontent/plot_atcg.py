'''
    plot base content
'''
#!/usr/bin/env python3
# coding: utf-8 -*-

import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import pandas as pd


__author__='Yuan Zan'
__mail__= 'seqyuan@gmail.com'


def get_df(file_path):
    df = pd.read_table(file_path, header=0)
    xlim = df[df['#']=='#total_reads'].index[0]
    df = df.loc[:xlim-1,:]
    df = df[['A','T','C','G','N']]

    df['total'] = df['A'] + df['T'] + df['C'] + df['G'] + df['N']
    df['A'] = df['A']*100/df['total']
    df['T'] = df['T']*100/df['total']
    df['C'] = df['C']*100/df['total']
    df['G'] = df['G']*100/df['total']
    df['N'] = df['N']*100/df['total']
    #df['GC'] = df['G'] + df['C']
    return df, xlim


def plot_line(ax, df):
    ax.plot(df.index, df['A'], color='y', marker='o', markersize=1, linewidth=1, alpha=1, label='A%')
    ax.plot(df.index, df['T'], color='g', marker='o', markersize=1, linewidth=1, alpha=1, label='T%')
    ax.plot(df.index, df['C'], color='r', marker='o', markersize=1, linewidth=1, alpha=1, label='C%')
    ax.plot(df.index, df['G'], color='b', marker='o', markersize=1, linewidth=1, alpha=1, label='G%')
    ax.plot(df.index, df['N'], color='grey', marker='o', markersize=1, linewidth=1, alpha=1, label='N%')
    #ax.plot(df['GC'], color='purple', linewidth=1, alpha=0.6)
    ax.spines['bottom'].set_color('black')
    ax.spines['bottom'].set_linewidth(1)
    ax.set_ylim(-5,70)

def main(args):
    file1, file2, outfile = args

    fig = plt.figure(figsize=(8, 4))
    [ax_x, ax_y, ax_w, ax_h] = [0.1,0.1,0.5,0.8]
    ax1 = fig.add_axes([0.1, 0.15, 0.4, 0.7], frame_on=True, facecolor = 'white')
    ax2 = fig.add_axes([0.5, 0.15, 0.4, 0.7], frame_on=True, facecolor = 'white')
    ax2.set_yticklabels([])
    ax2.set_yticks([])

    df1, xlim1 = get_df(file1)
    df2, xlim2 = get_df(file2)

    plot_line(ax1, df1)
    ax1.spines['left'].set_color('black')
    ax1.spines['left'].set_linewidth(1)
    ax1.set_xlim([-10,xlim1])
    ax1.set_ylabel("Percent(%)")
    ax1.set_xlabel("Reads1")

    plot_line(ax2, df2)
    ax2.set_xlim([xlim2,-10])
    ax2.set_xlabel("Reads2")

    ax1.axvline(x=xlim2, ls="-.", c="black", lw=1)
    ax2.axvline(x=xlim2, ls="-.", c="black", lw=1)

    legend = ax2.legend(bbox_to_anchor=(0.7, 1), loc=1, borderaxespad=0., prop={'size':8}, ncol=1, frameon=False)
    legend.get_frame().set_facecolor('white')


    plt.savefig(outfile)

def usage():
    sys.stderr.write('{0}\n\tAuthor:\t{1}\n\tEmail:\t{2}\n'.format(__doc__,__author__,__mail__))
    sys.stderr.write("\n\tusage:\n\t\tpython3 {0} R1.fq.gz.report R2.fq.gz.report outfile.pdf\n".format(__file__))
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage()
    main(sys.argv[1:])
    

