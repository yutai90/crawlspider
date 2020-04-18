# -*- coding: utf-8 -*-
#import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from zhilian.items import LagouItem
import time
import random
class LagoSpider(RedisCrawlSpider):
    name = 'lago'
    #allowed_domains = ['sou.zhaopin.com']
    #start_urls = ['http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC&kw=Python&sm=0&sg=653fa065e0974927aed1d54c6ae45bca&p=1']
    redis_key = 'lagospider:start_urls'
    rules = (
        Rule(LinkExtractor(allow=r'da42f04&p=\d+'), callback='parse_item', follow=True),

    )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(LagoSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        item = LagouItem()
        #也可以过滤每个岗位的链接（需要再写一个Rule），进入每个链接抓取信息，这样就不用循环了
        for table in response.xpath('//*[@id="newlist_list_content_table"]/table'):
            offer = table.xpath('string(.//tr[1]/td[1]/div/a)').extract()
            item['offername'] = self.get_offer(offer)
            item['_id'] = time.time() + random.random()
            yield item

    def get_offer(self,offer):
        if len(offer):
            return offer[0]
        else:
            return "NULL"
