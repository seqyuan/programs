#!/usr/bin/env python3
# coding: utf-8 -*- 
import sqlite3
import sys
import os
Bin = os.path.abspath(os.path.dirname(__file__))
#syscmd = 'export LANG=zh_CN.utf8'
#os.system(syscmd)

db = os.path.join(Bin,'applyProject.db')

drp_tb_sql = "drop table if exists applyProject"

crt_tb_sql = """
create table if not exists applyProject(
    id integer primary key autoincrement unique not null,
    user text,
    name text,    
    groups text,
    project_type text,
    project_name text,
    start_time text,
    end_time text,
    project_txt,
    need_time text
    );
"""

con = sqlite3.connect(db)
cur = con.cursor()
cur.execute(drp_tb_sql)
cur.execute(crt_tb_sql)


insert_sql = "insert into applyProject(user,name,groups,project_type,project_name,start_time,end_time,project_txt,need_time) values (?,?,?,?,?,?,?,?,?)"
cur.execute(insert_sql,('yuanzan','苑赞',"转录调控",'hic','Hi-C流程bug修复-交互频率图bug修改','2016/8/25','2016/08/26','小组立项申请程序编写','4'))

#update_sql = "update testdb set name = ?, email = ?, groups = ? where user = ?"
#cur.execute(update_sql,('张三','sanzhang@gmail.com','大组','zhangsan'))

con.commit()

select_sql = "select * from applyProject"

cur.execute(select_sql)
#返回一个list，list中的对象类型为tuple（元组）
date_set = cur.fetchall()
for row in date_set:
    print('\t'.join([str(i) for i in row]))

cur.close()
con.close()
