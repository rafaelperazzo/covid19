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
        self.writer.writerow(['data','id_ibge','cidade','gps','latitude','longitude','confirmado','suspeitos','obitos'])
        self.cariri = []
        #Abrir dicionario GPS
        arquivo_gps = open(OUTPUT_DIR + 'cidadeGPS.txt','r')
        latlon = arquivo_gps.read().replace("'","\"")
        arquivo_gps.close()
        self.dic_gps = json.loads(latlon)
        #Abrir dicionario ID
        arquivo_id = open('cidadeID.txt','r')
        ids = arquivo_id.read().replace("'","\"")
        arquivo_gps.close()
        self.dic_ids = json.loads(ids)

    def close_spider(self,spider):

        if (len(cidades_cariri)!=len(self.cariri)):
            for c in cidades_cariri:
                if (c not in self.cariri):
                    id_ibge = self.dic_ids[c]
                    gps = self.dic_gps[c]
                    latlon = self.dic_gps[c]
                    lista = latlon.split(',')
                    latitude = lista[0]
                    longitude = lista[1]
                    print(c)
                    self.writer.writerow([date.today().strftime("%Y-%m-%d"),id_ibge,c,gps,latitude,longitude,0,0,0])
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
        data = str(dic['data'])
        if (data==date.today().strftime("%Y-%m-%d")):
            if (cidade in cidades_cariri):
                if cidade not in self.cariri:
                    self.cariri.append(cidade)
        try:
            id_ibge = self.dic_ids[cidade]
            gps = self.dic_gps[cidade]
            latlon = self.dic_gps[cidade]
            lista = latlon.split(',')
            latitude = lista[0]
            longitude = lista[1]
            self.writer.writerow([dic['data'],id_ibge,cidade,gps,latitude,longitude,confirmados,suspeitos,obitos])
            #return item
        except KeyError:
            print("ERRO!")
            #return(item)
        finally:
            return (item)
