# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FundDetailItem(scrapy.Item):
    fund_id = scrapy.Field()
    one_week = scrapy.Field()
    one_month = scrapy.Field()
    three_month = scrapy.Field()
    six_month = scrapy.Field()
    since_year = scrapy.Field()
    one_year = scrapy.Field()
    two_year = scrapy.Field()
    three_year = scrapy.Field()
    one_week_rank = scrapy.Field()
    one_month_rank = scrapy.Field()
    three_month_rank = scrapy.Field()
    six_month_rank = scrapy.Field()
    since_year_rank = scrapy.Field()
    one_year_rank = scrapy.Field()
    two_year_rank = scrapy.Field()
    three_year_rank = scrapy.Field()
    update_time = scrapy.Field()

class FundInvest(scrapy.Item):
    fund_id = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    invest_count = scrapy.Field()
    start_money = scrapy.Field()
    end_money = scrapy.Field()
    invest_rate = scrapy.Field()
