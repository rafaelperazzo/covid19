# -*- coding: utf-8 -*-
import scrapy
from covid_ceara.items import CovidCearaItem
from datetime import date

class TodosSpider(scrapy.Spider):
    
    data_hoje = date.today().strftime("%Y-%m-%d")
    name = 'Todos'
    allowed_domains = ['https://apps.yoko.pet']
    start_urls = ['https://apps.yoko.pet/covid_csv/sec-ce-' + data_hoje + '.html']

    def parse(self, response):
        tabela = response.xpath('//*[@class="mat-table"]')
        linhas = tabela.xpath('//tr')
        for i in range(1,len(linhas),1):
            data = date.today().strftime("%Y-%m-%d")
            cidade = linhas[i].xpath('td//text()').extract()[0]
            confirmado = linhas[i].xpath('td//text()').extract()[1]
            suspeitos = linhas[i].xpath('td//text()').extract()[2]
            obitos = linhas[i].xpath('td//text()').extract()[3]
            entrada = CovidCearaItem(data=data,cidade=cidade,confirmado=confirmado,suspeitos=suspeitos,obitos=obitos)
            yield entrada
