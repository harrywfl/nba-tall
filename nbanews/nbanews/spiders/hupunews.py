# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup 
#必须将函数导进来，利用 from 项目名.items  import 类名
from nbanews.items import NbanewsItem

 #解析新闻主体的函数
def parseHtmlContent(htmlContent):
    newsContent = ''#用来拼接新闻主体的字符串
    soup = BeautifulSoup(htmlContent,'html.parser')
    #返回一个p标签的列表
    pList = soup.find_all('p')
    for p in pList:
        if p.string is None:
            continue
        else:
            newsContent += p.string #获取p标签的字符串
        return newsContent

#改进的解析新闻主体的函数
#def parseHtmlContent2(response):
#   newsContent = '' #用来拼接新闻主体的字符串
#   subSelector = response.xpath('//p/text()')
#   for each_sub in subSelector:
#       newsContent += each_sub.extract()
#   return newsContent

class HupunewsSpider(scrapy.Spider):
    name = "hupunews"
    allowed_domains = ["https://voice.hupu.com/nba"]
    #start_urls = ['https://voice.hupu.com/nba/']
    start_urls = []
    #默认爬取虎扑nba新闻前4页内容,
    for index in range(1,5):
        start_urls.append('https://voice.hupu.com/nba/'+str(index))

    def parse(self, response):
        items = [] #用来存放每次抓下来的一个新闻对象，由新闻标题，新闻时间和新闻url构成
        #找到每条新闻所在的位置，返回每个符合条件的新闻选择器的列表
        sub = response.xpath('//div[@class = "news-list"]/ul/li')
        #取出每一条新闻选择器，在选出其中的有用内容
        #测试用的
        for i in range(0,61):
        #因为每页有60个li
        #for i in range(0,61):
        	#第17个li里没有新闻，是个分割块，过滤掉
            if i == 16:
               continue
            else:
                #new 一个nba新闻爬取对象
                item = NbanewsItem()
                #获取新闻标题
                #if response.xpath('//div[@class = "news-list"]/ul/li/@class').extract()[0] == 'voice-ad690-90'
                item['newsTitle'] = sub[i].xpath('./div[@class="list-hd"]/h4/a/text()').extract()[0]
                #获取新闻url，因为extract方法返回的是一个列表，要获取其中唯一的元素，就必须加[0]
                newsUrl = sub[i].xpath('./div[@class="list-hd"]/h4/a/@href').extract()[0]
                #返回一个response对象
                r = requests.get(newsUrl)
                item['newsUrl'] = newsUrl
                #关键的问题是，怎么利用scrapy去根据爬取到的url继续爬取内容--->我们利用reauests库+bs4去爬取,里面有一个p标签的内容爬不出来
                #第一种方法
                item['newsContent'] = parseHtmlContent(r.text).replace('\xa0','')
                #获取新闻主体内容
                #改进的方法，能提取出第二个p标签的内容，但是还是不完善，em标签的内容没提出来
                #item['newsContent']  = parseHtmlContent2(r)
                #获取新闻时间
                newsTime = sub[i].xpath('./div[@class = "otherInfo"]/span[@class="other-left"]/a/@title').extract()[0]
                item['newsTime'] = newsTime
                #新闻平台ID，可以事先规定，假设我们虎扑平台的是1
                item['newsSrc'] = '1'
                #将每一个抓下来的新闻对象追加到对象列表中
                items.append(item)
        #返回新闻对象列表
        return items