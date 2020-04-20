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

cariri = ['ABAIARA', 'ALTANEIRA', 'ANTONINA DO NORTE', 'ARARIPE', 'ASSARE','AURORA','BARBALHA','BARRO', 'BREJO SANTO', 'CAMPOS SALES', 'CARIRIACU', 'CRATO', 'FARIAS BRITO', 'GRANJEIRO', 'JARDIM', 'JATI', 'JUAZEIRO DO NORTE', 'LAVRAS DA MANGABEIRA', 'MAURITI', 'MILAGRES', 'MISSAO VELHA', 'NOVA OLINDA', 'PENAFORTE', 'PORTEIRAS', 'POTENGI', 'SALITRE', 'SANTANA DO CARIRI', 'TARRAFAS', 'VARZEA ALEGRE']

headers = {
    'User-Agent': 'UFCAbot/1.0 Education Bot',
    'From': 'rafaelperazzo@gmail.com'
}

def prepararPalavra(palavra):

    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)

cidades_brasil = json.loads(requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/municipios',headers=headers).text)

cidades = []
for i in progressbar.progressbar(range(len(cidades_brasil))):
#for cidade in cidades_brasil:
    nome = prepararPalavra(cidades_brasil[i]['nome']).upper()
    estado = prepararPalavra(cidades_brasil[i]['microrregiao']['mesorregiao']['UF']['nome']).upper()
    id_estado = cidades_brasil[i]['microrregiao']['mesorregiao']['UF']['id']
    sigla_estado = prepararPalavra(cidades_brasil[i]['microrregiao']['mesorregiao']['UF']['sigla']).upper()
    id_ibge = cidades_brasil[i]['id']
    try:
        requisicao = json.loads(requests.get("https://nominatim.openstreetmap.org/search?city='" + nome + "'&format=json&state='" + estado + "'").text)
        time.sleep(1.2)
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
