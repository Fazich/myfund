# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spider.sqlutils.utils import connectSql

class FundDetailPipeline(object):
    db = ''
    def open_spider (self, spider):
        self.db = connectSql(True)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        if spider.name == 'fund_invest_calculate':
            self.cursor.execute('insert into fund_invest (fund_id, start_date, end_date, start_money, end_money, invest_rate) values (%s, %s, %s, %s, %s, %s)', (item['fund_id'], item['start_date'], item['end_date'], item['start_money'], item['end_money'], item['invest_rate']))
        elif spider.name == 'spider_detail':
            self.cursor.execute(
            'insert into fund_detail ( fund_id, one_week, one_month, three_month, six_month, since_year, one_year, two_year, three_year, one_week_rank, one_month_rank, three_month_rank, six_month_rank, since_year_rank, one_year_rank, two_year_rank, three_year_rank, update_time) values ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE update_time = %s', (item['fund_id'], item['one_week'], item['one_month'], item['three_month'], item['six_month'], item['since_year'], item['one_year'], item['two_year'], item['three_year'], item['one_week_rank'], item['one_month_rank'], item['three_month_rank'], item['six_month_rank'], item['since_year_rank'], item['one_year_rank'], item['two_year_rank'], item['three_year_rank'], item['update_time'], item['update_time']))

        self.db.commit()

    def close_spider(self, spider):
        self.db.close()

