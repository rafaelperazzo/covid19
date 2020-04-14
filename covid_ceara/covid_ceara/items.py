# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CovidCearaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    data = scrapy.Field()
    cidade = scrapy.Field()
    confirmado = scrapy.Field()
    suspeitos = scrapy.Field()
    obitos = scrapy.Field()
