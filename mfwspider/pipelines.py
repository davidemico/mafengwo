# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings

class MfwspiderPipeline(object):
    def process_item(self, item, spider):
        return item



class MongoPipeline(object):

    def __init__(self):

        conn = pymongo.MongoClient(host=settings['MONGO_HOST'],
                                   port=settings['MONGO_PORT'])
        self.db = conn[settings['MONGO_DB']]

    def process_item(self, item, spider):

        self.db[item.collections].update({'id':item.get('id')},{'$set':item},True)

        return item