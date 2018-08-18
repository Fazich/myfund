# -*- coding: UTF-8 -*-

import pymysql

def connectSql(state = False):
    print('连接到mysql服务器...')
    # 打开数据库连接
    # 用户名:hp, 密码:Hp12345.,用户名和密码需要改成你自己的mysql用户名和密码
    db = pymysql.connect("localhost","root","root","fund")
    print('连接上了!')
    return db if state == True else db.cursor()