#!/usr/bin/env python3
import sqlite3
import os
import sys
import pandas as pd


Bin = os.path.abspath(os.path.dirname(__file__))
db_file = "/abspath/Hi-C_stat.db"

conn = sqlite3.connect(db_file)
cur = conn.cursor()

writer = pd.ExcelWriter(os.path.join(os.getcwd(),'hicdb.xlsx'))

cur.execute("select name from sqlite_master where type='table' order by name")
all = cur.fetchall()
for n in range(len(all)):
    df = pd.read_sql("select * from \'{0}\'".format(all[n][0]), con=conn)
    df.to_excel(writer,sheet_name=all[n][0])

writer.close()
cur.close()
conn.close()


	
