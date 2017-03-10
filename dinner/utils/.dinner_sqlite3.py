#!/usr/bin/env pythin3
# coding: utf-8 -*- 
import sqlite3
import sys
import os
import re
import configparser
Bin = os.path.abspath(os.path.dirname(__file__))
sys.path.append(Bin + '/lib')
from dinnerEmail import myconf,select_usr

__author__='ahworld'
__mail__= 'leader@yodagene.com'

class myconf(configparser.ConfigParser):
    def __init__(self,defaults=None):
        configparser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        return optionstr

def test_exist(user):
    '''
    测试是否存在相同的记录
    '''
    sql_cmd = 'select * from dinnerusr where user = \'{0}\''.format(user)
    cur.execute(sql_cmd)
    theUser = cur.fetchall()

    if len(theUser) == 1:
        return (theUser)
    else:
        print ('update')


#def update_(cur,user):

usrDb = os.path.join(Bin,'usr.db')

conn = sqlite3.connect(usrDb)
cur = conn.cursor()
'''
select_sql = "select * from dinnerusr"
cur.execute(select_sql)
date_set = cur.fetchall()
for row in date_set:
    print(row)
'''
a = test_exist('ag')
#if a[0][4]:
 #   print (a[0])

def myinput(content):
    result = ''
    while(1):
        try:
            result = input('>>> ' + content)
            result = result.rstrip()
            if result == 'exit':
                sys.exit(0)
            else:
                return result.rstrip()
        except SystemExit : 
            print("程序退出，bye")
            sys.exit(0)
        except :
            print("格式错误，请重新输入")
            pass

def insert_sql(conn,cur,usr):
    name, mail, group = '', '', ''
    while(1):
        name = myinput('请输入你的姓名:\n')
        if name == '':
            print("不能为空")
        else:
            break
    mailpatt = re.compile('@yodagene.com$')
    while(1):
        mail = myinput('请输入你的邮箱:\n')
        if re.search(mailpatt , mail): break
    while(1):
        group = myinput('请输入你的组别,例如 分析组-RNA&表观组 or 研发组-医学DNA组:\n')
        if group == '':
            print("不能为空")
        else:
            break
    insert_sql = "insert into dinnerusr(user,name,email,groups,dinner) values (?,?,?,?,?)"
    cur.execute(insert_sql,(usr,name,mail,group,''))    
    conn.commit()

def update_sql(conn,cur,usr):
    idn, user, name, email, groups, dinner = select_usr(cur,usr)
    new_name, new_email, new_groups = '', '', ''
    if name == '':
        while(1):
            new_name = myinput('请输入你的姓名:\n')
            if new_name == '':
                print("不能为空")
            else:
                break
    else:
        print ('你的姓名已存在 {0},不需要更改请直接按回车键'.format(name))
        new_name = myinput('请输入你的姓名:\n')
    if new_name != '': name = new_name

    mailpatt = re.compile('@yodagene.com$')
    if email == '':
        while(1):
            new_email = myinput('请输入你的邮箱:\n')
            if re.search(mailpatt , new_email): 
                break
            else:
                print("不能为空")
    else:
        print ('你的邮箱已存在 {0},不需要更改请直接按回车键'.format(email))
        new_email = myinput('请输入你的邮箱:\n')
    if new_email != '': email = new_email

    if groups == '':
        while(1):
            new_groups = myinput('请输入你的组别,例如 分析组-RNA&表观组 or 研发组-医学DNA组:\n')
            if new_groups == '':
                print("不能为空")
            else:
                break
    else:
        print ('你的组名已存在 {0},不需要更改请直接按回车键'.format(groups))
        new_groups = myinput('请输入你的组别,例如 分析组-RNA&表观组 or 研发组-医学DNA组:\n')
    if new_groups != '': groups = new_groups    

    update_sql = "update dinnerusr set name = \'{0}\', email = \'{1}\', groups = \'{2}\' where user = \'{3}\'".format(name,email,groups,usr)
    cur.execute(update_sql)    
    conn.commit()

#delete_sql = 'delete from dinnerusr where user = \'{0}\''.format('yuanzan')
#cur.execute(delete_sql)
#insert_sql(conn,cur,'yuanzan')
update_sql(conn,cur,'ahworld')

select_sql = "select * from dinnerusr"
cur.execute(select_sql)
date_set = cur.fetchall()
for row in date_set:
    print(row)

cur.close()
conn.close()

