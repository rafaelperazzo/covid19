# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import date
import csv
import json
OUTPUT_DIR = '/dados/flask/cimai/covid/'

def removeChar(s):

    r = s.replace('"','')
    r = r.replace(',','')
    r = r.replace('.','')
    return(int(r))


class CovidCearaPipeline(object):

    def open_spider(self,spider):
        today = date.today()
        data_hoje = today.strftime("%Y-%m-%d")
        self.file = open(OUTPUT_DIR + 'TODOS.CEARA.HOJE.CSV', 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['data','cidade','confirmado','suspeitos','obitos'])


    def close_spider(self,spider):
        self.file.close()

    def process_item(self, item, spider):
        #https://www.w3schools.in/python-tutorial/remove-space-from-a-string-in-python/
        dic = dict(item)
        confirmados = removeChar(str(dic['confirmado']))
        suspeitos = removeChar(str(dic['suspeitos']))
        obitos = removeChar(str(dic['obitos']))
        self.writer.writerow([dic['data'],dic['cidade'],confirmados,suspeitos,obitos])
        return item
