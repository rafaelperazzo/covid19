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
from sqlalchemy import create_engine

DB = '/dados/flask/cimai/covid/cidades.sqlite3'
DB_HOJE = '/dados/flask/cimai/covid/dados.cariri.hoje.sqlite3'
OUTPUT_DIR = '/dados/flask/cimai/covid/'
sys.path.insert(0,'/dados/flask/cimai/covid')

import slDB as sq

def atualizarDados(conexao=None,id=0,cidade='indefinida',confirmados=0,suspeitos=0,obitos=0,taxa=0,populacao=0,recuperados=0):    
    consulta = 'INSERT INTO hoje(id,cidade,confirmados,suspeitos,obitos,taxa,populacao,recuperados) VALUES (?,?,?,?,?,?,?,?)'
    conexao.execute(consulta,[id,cidade,confirmados,suspeitos,obitos,taxa,populacao,recuperados])

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
        self.writer.writerow(['data','id_ibge','cidade','gps','latitude','longitude','confirmado','suspeitos','obitos','populacao','recuperados'])
        self.cariri = []

        #sqlite
        self.conn = sq.MyDB(DB,'ceara')
        self.engine = create_engine('sqlite:///' + DB_HOJE, echo=False)
        self.connHoje = self.engine.connect()
        self.connHoje.execute('DROP TABLE IF EXISTS hoje')
        self.connHoje.execute('CREATE TABLE hoje (id INT, cidade TEXT, confirmados INT, suspeitos INT, obitos INT, taxa FLOAT, populacao INT,recuperados INT)')

    def close_spider(self,spider):

        if (len(cidades_cariri)!=len(self.cariri)):
            for c in cidades_cariri:
                if (c not in self.cariri):
                    id_ibge = self.conn.getIDFromName(c)
                    gps = self.conn.getGPSFromID(id_ibge)
                    populacao = self.conn.getPopulacaoFromID(id_ibge)
                    latitude = self.conn.getLatitudeFromID(id_ibge)
                    longitude = self.conn.getLongitudeFromID(id_ibge)
                    atualizarDados(self.connHoje,id_ibge,c,0,0,0,0,int(populacao))
                    self.writer.writerow([date.today().strftime("%Y-%m-%d"),id_ibge,c,gps,latitude,longitude,0,0,0,populacao,0])

        self.file.close()
        #sqlite3
        self.conn.close()
        self.connHoje.close()
        


    def process_item(self, item, spider):
        #https://www.w3schools.in/python-tutorial/remove-space-from-a-string-in-python/
        dic = dict(item)
        confirmados = removeChar(str(dic['confirmado']))
        suspeitos = removeChar(str(dic['suspeitos']))
        recuperados = removeChar(str(dic['recuperados']))
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
            
            #Inserindo os dados da data atual
            if (data==date.today().strftime("%Y-%m-%d")):
                if (cidade in cidades_cariri):
                    taxa = round((int(confirmados-recuperados)/int(populacao))*100000,2)
                    atualizarDados(self.connHoje,id_ibge,cidade,int(confirmados),int(suspeitos),int(obitos),taxa,int(populacao),int(recuperados))
            self.writer.writerow([dic['data'],id_ibge,cidade,gps,latitude,longitude,confirmados,suspeitos,obitos,populacao,recuperados])

        except KeyError:
            print("ERRO!")

        finally:
            return (item)
