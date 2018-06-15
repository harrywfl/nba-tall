# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NbanewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #新闻标题
    newsTitle = scrapy.Field()
    #新闻时间
    newsTime = scrapy.Field()
    #新闻url
    newsUrl = scrapy.Field()
    #新闻内容
    newsContent = scrapy.Field()
    #新闻来源平台
    newsSrc = scrapy.Field()
