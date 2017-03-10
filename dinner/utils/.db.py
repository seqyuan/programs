#!/usr/bin/env pythin3
# coding: utf-8 -*- 
import sqlite3
import sys
import os
import re
import configparser
Bin = os.path.abspath(os.path.dirname(__file__))
#syscmd = 'export LANG=zh_CN.utf8'

#os.system(syscmd)
import time
import getpass

__author__='ahworld'
__mail__= 'leader@yodagene.com'

pat1=re.compile('^\s*$')

class myconf(configparser.ConfigParser):
    def __init__(self,defaults=None):
        configparser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        return optionstr


config=myconf()
config.readfp(open(os.path.join(Bin,'dinner.ini'),encoding='utf-8'))

#username = getpass.getuser()

db = os.path.join(Bin,'usr.db')

drp_tb_sql = "drop table if exists dinnerusr"
crt_tb_sql = """
create table if not exists dinnerusr(
    id integer primary key autoincrement unique not null,
    user unique not null,
    name text,
    email text,
    groups text,
    dinner text
    );
"""
con = sqlite3.connect(db)
cur = con.cursor()

#cur.execute(drp_tb_sql)
#cur.execute(crt_tb_sql)

insert_sql = "insert into dinnerusr(user,name,email,groups,dinner) values (?,?,?,?,?)"

for usr in config.items('usrname'):
    #print (usr)
    groups = ''
    if config.has_option('group',usr[0]):
        groups = config.get('group',usr[0])

    #cur.execute(insert_sql,(usr[0],usr[1],config.get('usrmail',usr[0]),groups,''))

con.commit()

select_sql = "select * from dinnerusr"

cur.execute(select_sql)
#返回一个list，list中的对象类型为tuple（元组）
date_set = cur.fetchall()
for row in date_set:
    print(row)

cur.close()
con.close()
