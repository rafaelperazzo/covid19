# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import date
import csv
import json
OUTPUT_DIR = '/dados/flask/cimai/covid/'

class CovidCearaPipeline(object):

    def open_spider(self,spider):
        today = date.today()
        data_hoje = today.strftime("%Y-%m-%d")
        self.file = open(OUTPUT_DIR + 'sec-ce-' + data_hoje +'.json', 'w')
        #self.writer = csv.writer(self.file)
        #self.writerow(['cidade','confirmado','suspeitos','obitos'])

    def close_spider(self,spider):
        self.file.close()

    def process_item(self, item, spider):
        linha = json.dumps(dict(item)) + '\n'
        self.file.write(linha)
        return item
