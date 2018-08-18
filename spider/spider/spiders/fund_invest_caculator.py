# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from ..items import FundInvest
from urllib.parse import urljoin
from ..sqlutils.utils import connectSql


class FundInvestCaculatorSpider(scrapy.Spider):
    name = 'fund_invest_calculate'
    allowed_domains = ['http://fund.eastmoney.com/']
    db = ''
    def start_requests(self):
        base_url = 'http://fund.eastmoney.com/data/FundInvestCaculator_AIPDatas.aspx'
        fund_list = self.get_fund_list(70, 70, 70, 70)
        date_list = self.generate_date_list('2015-01-01')
        for fund in fund_list:
            fund_id = fund[0]
            self.logger.info('基金'+ fund_id + '定投数据爬取中')
            for date in date_list:
                start_date = date.get('start_date')
                end_date = date.get('end_date')
                request_url = urljoin(base_url, '?fcode={0}&sdate={1}&edate={2}&shdate=&round=-7&dtr=1&p=0.15&je=500&stype=2&needfirst=2'.format(fund_id, start_date, end_date))
                yield scrapy.Request(request_url, meta={'start_date': start_date, 'end_date': end_date})
        pass

    def parse(self, response):
        data = str(response.body).split('|')
        item = FundInvest()
        item['fund_id'] = re.sub('\D', '', data[0])
        item['start_money'] = data[3]
        item['end_money'] = data[5]
        item['invest_rate'] = data[6].replace('%', '')
        item['start_date'] = response.meta['start_date']
        item['end_date'] = response.meta['end_date']
        if item['start_money'] != '0.00' and item['end_money'] != '0.00':
            yield item

    def get_fund_list(self, since_rank, one_year_rank, two_year_rank, three_year_rank):
        self.db = connectSql()
        self.db.execute('select fund_id from fund_detail where since_year_rank > %s and one_year_rank > %s and two_year_rank > %s and three_year_rank > %s;', (since_rank, one_year_rank, two_year_rank, three_year_rank))
        return self.db.fetchall()

    # 生成定投日期序列
    def generate_date_list(self, start):
        date_list = []
        date_now = datetime.datetime.today()
        start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
        end_date = start_date + datetime.timedelta(days = 365)
        while end_date <= date_now:
            date_list.append({
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            })
            start_date = start_date + datetime.timedelta(days = 7)
            end_date = start_date + datetime.timedelta(days = 365)

        return date_list




