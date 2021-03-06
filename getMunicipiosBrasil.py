# -*- coding: utf-8 -*-
'''
Fonte: https://servicodados.ibge.gov.br/api/docs/localidades?versao=1
'''
import requests
import json
import unicodedata
import re
import progressbar
import pandas as pd
import time

HOME_DIR = '/dados/flask/cimai/covid/'

cariri = ['ABAIARA', 'ALTANEIRA', 'ANTONINA DO NORTE', 'ARARIPE', 'ASSARE','AURORA','BARBALHA','BARRO', 'BREJO SANTO', 'CAMPOS SALES', 'CARIRIACU', 'CRATO', 'FARIAS BRITO', 'GRANJEIRO', 'JARDIM', 'JATI', 'JUAZEIRO DO NORTE', 'LAVRAS DA MANGABEIRA', 'MAURITI', 'MILAGRES', 'MISSAO VELHA', 'NOVA OLINDA', 'PENAFORTE', 'PORTEIRAS', 'POTENGI', 'SALITRE', 'SANTANA DO CARIRI', 'TARRAFAS', 'VARZEA ALEGRE']

headers = {
    'User-Agent': 'UFCAbot/1.0 Education Bot',
    'From': 'rafaelperazzo@gmail.com'
}

def prepararPalavra(palavra):

    nfkd = unicodedata.normalize('NFKD', palavra).encode('ASCII','ignore').decode('ASCII')
    return(nfkd.upper())

cidades_brasil = json.loads(requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/municipios',headers=headers).text)

cidades = []
for i in progressbar.progressbar(range(len(cidades_brasil))):
#for cidade in cidades_brasil:
    nome = prepararPalavra(cidades_brasil[i]['nome'])
    estado = prepararPalavra(cidades_brasil[i]['microrregiao']['mesorregiao']['UF']['nome'])
    id_estado = cidades_brasil[i]['microrregiao']['mesorregiao']['UF']['id']
    sigla_estado = prepararPalavra(cidades_brasil[i]['microrregiao']['mesorregiao']['UF']['sigla'])
    id_ibge = cidades_brasil[i]['id']
    try:
        requisicao = json.loads(requests.get("https://nominatim.openstreetmap.org/search?city='" + nome + "'&format=json&state='" + estado + "'").text)
        time.sleep(1.2) #não mude, pois você poderá ser bloqueado ou banido da API
        latitude = requisicao[0]['lat']
        longitude = requisicao[0]['lon']
        gps = str(latitude) + ',' + str(longitude)
    except (IndexError,json.decoder.JSONDecodeError) as e:
        latitude = 0
        longitude = 0
        gps = "0,0"
        print(e)
        print(nome)
        print(estado)

    item = {"id": id_ibge, "cidade": nome,"id_estado": id_estado,"sigla": sigla_estado,"estado": estado ,"gps": gps, "latitude": latitude,"longitude": longitude}
    cidades.append(item)

j = json.dumps(cidades)
df_json = pd.read_json(j)
df_json = df_json[['id','cidade','id_estado','sigla','estado','latitude','longitude','gps']]
df_json.to_csv('cidades.brasil.completo.csv',index=False)

populacao = pd.read_csv(HOME_DIR + 'municipios.populacao.2019.csv',dtype={'id_uf':str,'id_ibge':str})
cidades = pd.read_csv(HOME_DIR + 'cidades.brasil.completo.csv')

uf = populacao['id_uf']
populacao['id_ibge'] = populacao['id_ibge'].str.pad(width=5,fillchar='0',side='left')
populacao['id'] = populacao['id_uf'] + populacao['id_ibge']
populacao['id'] = populacao['id'].astype(int)
populacao.drop(['id_ibge'],axis=1,inplace=True)
populacao = populacao[['id','populacao']]
cidades = pd.merge(cidades,populacao,on='id')
cidades.to_csv(HOME_DIR + 'cidades.brasil.completo.csv',index=False,float_format='%.7f')
print("PROCEDIMENTO TERMINADO COM SUCESSO!")
