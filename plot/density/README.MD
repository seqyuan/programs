# 说明
### 读入一个tab分隔的文件，对每一列的数值取log2，然后计算每一列的density，做出每一列的density曲线
# 使用方法
`python3 density.py fpkm.xls Distribution_of_Sample_Expression.png 'Distribution of Sample Expression' 'log2FPKM'`
# 输入文件格式
  name | D1	| D2 |	D3	| E1 |	E2 |	E3 
  :-------- | :--------|:--------|:--------|:--------|:--------|:--------
 gene027601	| 10.47	| 10.66	| 10.93 |	10.46	| 9.99 |	11.56 
 gene034858	| 2.45	| 2.45	| 2.32	| 1.85	| 1.85	| 1.5|
 gene013593	| 119.11 |	116.56	| 114.39 |	76.34 |	77.96	| 78.1 

# 结果示例
 ![结果示例](./Distribution_of_Sample_Expression.png)