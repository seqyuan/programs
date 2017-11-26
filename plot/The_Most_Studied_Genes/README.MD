# 复现"The most popular genes in the human genome"

 为了做matplotlib画图笔记,记录一些常用画图设置模板,我下载了The most popular genes in the human genome(doi: 10.1038/d41586-017-07291-9)中人类基因组基因研究文章的统计数据: gene_info_total_human.tsv(包含所有基因组元件研究信息),all_gene_counts.tsv(只包含基因的研究信息,包含基因位置信息),以及染色体大小文件http://hgdownload.cse.ucsc.edu/goldenpath/hg19/database/chromInfo.txt.gz,复现了其中两幅图

## 使用方法

`python3 The_Most_Studied_Genes.py -i gene_info_total_human.tsv -n 20`

## 结果示例1
 ![结果示例1](./The_top_citations.png)
