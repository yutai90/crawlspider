# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#进行分布式的时候不经过此管道文件
import pymongo

class LagouPipeline(object):
    def process_item(self, item, spider):
        client = pymongo.MongoClient('localhost',27017)
        db = client['zhaopin']
        collection = db['zhilian']
        collection.insert_one(item)
        return item
