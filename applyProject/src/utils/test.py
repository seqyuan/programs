#!/usr/bin/env python3
#coding: utf-8
import os
Bin = os.path.abspath(os.path.dirname(__file__))

import sqlite3

conn = sqlite3.connect(os.path.join(Bin,'applyProject.db'))
cur = conn.cursor()


'''
cursor = conn.execute("select email from usrInfo where groups = \'{0}\'".format('转录调控组'))
str = ";"
to = ''
#to = str.join(cursor.fetchall())
to = ';'.join([i[0] for i in cursor.fetchall()])

print (to)
#select_sql = 'select name, groups from usrInfo where user = \'{0}\''.format(username)
#cur.execute(select_sql)
#for row in cursor:
#	print (row[0])
#	print (row[1])
'''
cursor = conn.execute("select * from usrInfo where groups = \'{0}\'".format('转录调控组'))
for i in cursor.fetchall():
    print (i)
cur.close()
conn.close()
