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
import sys

DB = '/dados/flask/cimai/covid/cidades.sqlite3'
OUTPUT_DIR = '/dados/flask/cimai/covid/'
sys.path.insert(0,'/dados/flask/cimai/covid')

import slDB as sq

def removeChar(s):

    r = s.replace('"','')
    r = r.replace(',','')
    r = r.replace('.','')
    return(int(r))

cidades_cariri = ['ABAIARA', 'ALTANEIRA', 'ANTONINA DO NORTE', 'ARARIPE', 'ASSARE','AURORA','BARBALHA','BARRO', 'BREJO SANTO', 'CAMPOS SALES', 'CARIRIACU', 'CRATO', 'FARIAS BRITO', 'GRANJEIRO', 'JARDIM', 'JATI', 'JUAZEIRO DO NORTE', 'LAVRAS DA MANGABEIRA', 'MAURITI', 'MILAGRES', 'MISSAO VELHA', 'NOVA OLINDA', 'PENAFORTE', 'PORTEIRAS', 'POTENGI', 'SALITRE', 'SANTANA DO CARIRI', 'TARRAFAS', 'VARZEA ALEGRE']

def prepararPalavra(palavra):

    nfkd = unicodedata.normalize('NFKD', palavra).encode('ASCII','ignore').decode('ASCII')
    return(nfkd.upper())

class CovidCearaPipeline(object):

    def open_spider(self,spider):
        today = date.today()
        data_hoje = today.strftime("%Y-%m-%d")
        self.file = open(OUTPUT_DIR + 'TODOS.CEARA.HOJE.CSV', 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['data','id_ibge','cidade','gps','latitude','longitude','confirmado','suspeitos','obitos','populacao'])
        self.cariri = []

        #sqlite
        self.conn = sq.MyDB(DB,'ceara')

    def close_spider(self,spider):

        if (len(cidades_cariri)!=len(self.cariri)):
            for c in cidades_cariri:
                if (c not in self.cariri):
                    id_ibge = self.conn.getIDFromName(c)
                    gps = self.conn.getGPSFromID(id_ibge)
                    populacao = self.conn.getPopulacaoFromID(id_ibge)
                    latitude = self.conn.getLatitudeFromID(id_ibge)
                    longitude = self.conn.getLongitudeFromID(id_ibge)
                    self.writer.writerow([date.today().strftime("%Y-%m-%d"),id_ibge,c,gps,latitude,longitude,0,0,0,populacao])

        self.file.close()
        #sqlite3
        self.conn.close()


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
        data = str(dic['data'])
        if (data==date.today().strftime("%Y-%m-%d")):
            if (cidade in cidades_cariri):
                if cidade not in self.cariri:
                    self.cariri.append(cidade)
        try:
            id_ibge = self.conn.getIDFromName(cidade)
            gps = self.conn.getGPSFromID(id_ibge)
            populacao = self.conn.getPopulacaoFromID(id_ibge)
            latitude = self.conn.getLatitudeFromID(id_ibge)
            longitude = self.conn.getLongitudeFromID(id_ibge)

            self.writer.writerow([dic['data'],id_ibge,cidade,gps,latitude,longitude,confirmados,suspeitos,obitos,populacao])

        except KeyError:
            print("ERRO!")

        finally:
            return (item)
