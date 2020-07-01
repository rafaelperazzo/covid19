# -*- coding: utf-8 -*-
import scrapy
from covid_ceara.items import CovidCearaItem
from datetime import date
import datetime

URL = 'https://apps.yoko.pet/covid_csv/spyder/sec-ce-'

def getURLs(inicio):
    start = datetime.datetime.strptime(inicio, "%Y-%m-%d")
    end = datetime.datetime.strptime(date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]
    lista = []
    for data in date_generated:
        dia = data.strftime("%Y-%m-%d")
        lista.append(URL + dia + '.html')
    return(lista)

def getDataFromURL(url):
    resultado = url[len(URL):]
    resultado = resultado[:-5]
    return(resultado)

class TodosSpider(scrapy.Spider):

    data_hoje = date.today().strftime("%Y-%m-%d")
    name = 'Todos'
    allowed_domains = ['https://apps.yoko.pet']
    #start_urls = ['https://apps.yoko.pet/covid_csv/sec-ce-' + data_hoje + '.html']
    start_urls = getURLs('2020-03-01')

    def parse(self, response):
        tabela = response.xpath('//*[@class="mat-table"]')
        if len(tabela)==0:
            tabela = response.xpath('//*[@class="mat-table cdk-table mat-sort"]')
        linhas = tabela.xpath('//tr')
        for i in range(1,len(linhas),1):
            #data = date.today().strftime("%Y-%m-%d")
            data = getDataFromURL(response.request.url)
            cidade = linhas[i].xpath('td//text()').extract()[0]
            confirmado = linhas[i].xpath('td//text()').extract()[1]
            suspeitos = linhas[i].xpath('td//text()').extract()[2]
            recuperados = linhas[i].xpath('td//text()').extract()[4]
            try:
                obitos = linhas[i].xpath('td//text()').extract()[5]
            except IndexError:
                obitos = linhas[i].xpath('td//text()').extract()[3]
            entrada = CovidCearaItem(data=data,cidade=cidade,confirmado=confirmado,suspeitos=suspeitos,obitos=obitos,recuperados=recuperados)
            yield entrada
