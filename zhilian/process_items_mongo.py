# -*-coding:utf-8-*-

import redis
import json
import pymongo

def process_items():
    #创建redis数据库连接，redis若是本地，则host = "127.0.0.1"
    rediscli = redis.Redis(host= "192......", port=6379,db= 0)
    #创建MongoDB的链接
    mongocli = pymongo.MongoClient(host= "127.0.0.1", port=27017)
    #连接数据库
    db = mongocli['zhaopin']
    #连接数据表
    collection = db["zhilian"]
    offset = 0

    while True:
        #读取redis,source里放db的name，data放items
        source, data = rediscli.blpop("lago:items")
        offset += 1
        #将json对象转化成Python对象
        data = json.loads(data)
        #将数据插入到MongoDB的表中
        data['_id'] = offset
        collection.insert_one(data)
        print offset


if __name__ == '__main__':
    process_items()
