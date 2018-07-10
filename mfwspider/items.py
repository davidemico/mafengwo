# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MfwspiderItem(scrapy.Item):

    collections = 'gonglve'

    id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    imageUrl = scrapy.Field()
    travelTime =scrapy.Field()
    price = scrapy.Field()
    tips = scrapy.Field()


