# -*- coding: utf-8 -*-
import scrapy
import time
import json
from urllib.parse import urljoin
from ..items import FundDetailItem
from ..sqlutils.utils import connectSql
from ..sqlutils.sql import sql

class SpiderDetailSpider(scrapy.Spider):
    name = 'spider_detail'
    allowed_domains = ['fund.10jqka.com.cn']
    db = ''
    def start_requests(self):
        self.db = connectSql()
        self.db.execute(sql.get('get_all_fund'))
        base_url = 'http://fund.10jqka.com.cn/ifindRank/'
        all_fund = self.db.fetchall()
        for fund in all_fund:
            yield scrapy.Request(urljoin(base_url, 'quarter_year_{fund_id}.json'.format(fund_id = fund[0])), meta={'fund_id': fund[0]})

    def parse(self, response):
        item = FundDetailItem()
        data = json.loads(response.body)
        try:
            item['fund_id'] = response.meta['fund_id']
            item['one_week'] = data.get('nowFqNetRate').get('week')
            item['one_month'] = data.get('nowFqNetRate').get('month')
            item['three_month'] = data.get('nowFqNetRate').get('tmonth')
            item['six_month'] = data.get('nowFqNetRate').get('hyear')
            item['since_year'] = data.get('nowFqNetRate').get('nowyear')
            item['one_year'] = data.get('nowFqNetRate').get('year')
            item['two_year'] = data.get('nowFqNetRate').get('twoyear')
            item['three_year'] = data.get('nowFqNetRate').get('tyear')
            item['one_week_rank'] = data.get('nowCommonTypeRank').get('week')[2]
            item['one_month_rank'] = data.get('nowCommonTypeRank').get('month')[2]
            item['three_month_rank'] = data.get('nowCommonTypeRank').get('tmonth')[2]
            item['six_month_rank'] = data.get('nowCommonTypeRank').get('hyear')[2]
            item['since_year_rank'] = data.get('nowCommonTypeRank').get('nowyear')[2]
            item['one_year_rank'] = data.get('nowCommonTypeRank').get('year')[2]
            item['two_year_rank'] = data.get('nowCommonTypeRank').get('twoyear')[2]
            item['three_year_rank'] = data.get('nowCommonTypeRank').get('tyear')[2]
            item['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.logger.info('基金' + item['fund_id'] + '爬取成功')
            yield item
        except:
            self.logger.error('基金' + item['fund_id'] + '字段不全')

    def closed(self,reason):
        self.db.close()
