# -*- coding: utf-8 -*-

import scrapy


class SecondItem(scrapy.Item):
    passage = scrapy.Field()
    # view = scrapy.Field()


class NewsItem(scrapy.Item):
    headline = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()
    passage = scrapy.Field()
    read_num = scrapy.Field()#阅读量
    labels = scrapy.Field()#文章标签
    likes = scrapy.Field()#文章获赞数
    comments = scrapy.Field()#文章评论数
    author_followers = scrapy.Field()#粉丝数
    author_publishes = scrapy.Field()#发文数
    author_views = scrapy.Field()#浏览数
    btc_price = scrapy.Field()#发文时btc价格
    '''passage = scrapy.Field()
    response = scrapy.Field()'''
