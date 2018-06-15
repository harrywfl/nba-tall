# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import json
import codecs

class NbanewsPipeline(object):
    #怎么处理提取到的新闻
    def process_item(self, item, spider):
        today = time.strftime('%Y-%m-%d-%H',time.localtime())#返回指定格式的时间字符串，年-月-日，用来做文件名称
        fileName = today + '.json'
        #先将items里的文件写入到txt文本里,已追加的方式写,一行为一个item，写完之后换行，item的内部元素之间以制表符\t隔开
        with codecs.open(fileName,'a',encoding = 'utf8') as f:
            line = json.dumps(dict(item),ensure_ascii=False)+'\n'
            f.write(line)
            time.sleep(2)
        return item;