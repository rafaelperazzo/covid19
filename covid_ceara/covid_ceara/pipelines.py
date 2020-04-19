# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import date
import csv
import json
import unicodedata
import re

OUTPUT_DIR = '/dados/flask/cimai/covid/'

def removeChar(s):

    r = s.replace('"','')
    r = r.replace(',','')
    r = r.replace('.','')
    return(int(r))

cidades_cariri = ['ABAIARA', 'ALTANEIRA', 'ANTONINA DO NORTE', 'ARARIPE', 'ASSARE','AURORA','BARBALHA','BARRO', 'BREJO SANTO', 'CAMPOS SALES', 'CARIRIACU', 'CRATO', 'FARIAS BRITO', 'GRANJEIRO', 'JARDIM', 'JATI', 'JUAZEIRO DO NORTE', 'LAVRAS DA MANGABEIRA', 'MAURITI', 'MILAGRES', 'MISSAO VELHA', 'NOVA OLINDA', 'PENAFORTE', 'PORTEIRAS', 'POTENGI', 'SALITRE', 'SANTANA DO CARIRI', 'TARRAFAS', 'VARZEA ALEGRE']

def prepararPalavra(palavra):

    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)

class CovidCearaPipeline(object):

    def open_spider(self,spider):
        today = date.today()
        data_hoje = today.strftime("%Y-%m-%d")
        self.file = open(OUTPUT_DIR + 'TODOS.CEARA.HOJE.CSV', 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['data','cidade','confirmado','suspeitos','obitos'])
        self.cariri = []

    def close_spider(self,spider):

        if (len(cidades_cariri)!=len(self.cariri)):
            for c in cidades_cariri:
                if (c not in self.cariri):
                    self.writer.writerow([date.today().strftime("%Y-%m-%d"),c,0,0,0])
        self.file.close()

    def process_item(self, item, spider):
        #https://www.w3schools.in/python-tutorial/remove-space-from-a-string-in-python/
        dic = dict(item)
        confirmados = removeChar(str(dic['confirmado']))
        suspeitos = removeChar(str(dic['suspeitos']))
        obitos = removeChar(str(dic['obitos']))
        cidade = str(dic['cidade'])
        cidade = cidade.lstrip()
        cidade = cidade.rstrip()
        cidade = prepararPalavra(cidade)
        if (cidade in cidades_cariri):
            if cidade not in self.cariri:
                self.cariri.append(cidade)
        self.writer.writerow([dic['data'],cidade,confirmados,suspeitos,obitos])
        return item
