# -*- coding: UTF-8 -*-

import pymysql
import datetime
import numpy as np

class Static():
    def __init__(self):
        self.db = ''
        self.cursor =''
        self.data_list =''
        self.calculate_date = dict()
        self.run()

    def connectSql(self):
        print('连接到mysql服务器...')
        # 打开数据库连接
        # 用户名:hp, 密码:Hp12345.,用户名和密码需要改成你自己的mysql用户名和密码
        db = pymysql.connect("localhost","root","root","fund")
        print('连接上了!')
        self.db = db
        self.cursor = db.cursor()

    def get_data_list(self):
        self.cursor.execute('SELECT fund_id,invest_rate FROM fund_invest ORDER BY fund_id ,start_date;')
        self.data_list = self.cursor.fetchall()

    def sort_data_list(self):
        for data in self.data_list:
            fund_id = data[0]
            rate = data[1]
            self.calculate_date.setdefault(fund_id, []).append(rate)

    def static(self):
        for fund_id in self.calculate_date:
            npa = np.array(self.calculate_date[fund_id])
            average = float(round(np.mean(npa),2))
            median = float(round(np.median(npa),2))
            variance = float(round(np.var(npa),2))
            max_rate = float(round(np.max(npa),2))
            min_rate = float(round(np.min(npa),2))
            standard = float(round(np.std(npa),2))
            update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print('基金' + fund_id + '存储中')
            self.cursor.execute('INSERT INTO fund_static (fund_id, min_rate, max_rate, average, standard, variance, median, update_time) values ( %s, %s, %s, %s, %s, %s, %s, %s)',(fund_id, min_rate, max_rate, average, standard, variance, median, update_time))
            self.db.commit()



    def run(self):
        self.connectSql()
        self.get_data_list()
        self.sort_data_list()
        self.static()


Static()


