# -*- coding: utf-8 -*-
import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from time import sleep
import csv
from datetime import date
import os
import glob

#Fonte: https://github.com/wcota/covid19br
#Fonte: Ministério da Saúde
#Fonte: Secretaria de Saúde/CE

CSV_DIR = '/dados/flask/cimai/covid/'

today = date.today()
data_hoje = today.strftime("%Y-%m-%d")

url = 'https://indicadores.integrasus.saude.ce.gov.br/indicadores/indicadores-coronavirus/coronavirus-ceara'
url_ministerio = 'https://covid.saude.gov.br/'
url_wcota_cidades = 'https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv'
url_wcota_gps = 'https://raw.githubusercontent.com/wcota/covid19br/master/cases-gps.csv'

#OPCOES
options = Options()
options.headless = True
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", CSV_DIR)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

#abrindo o navegador
driver = webdriver.Firefox(options=options,firefox_profile=profile)
#BAIXANDO DA SECRETARIA DA SAUDE/CE
driver.get(url)
sleep(3)
webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
sleep(2)
botao = driver.find_element_by_class_name("mat-select-arrow-wrapper")
botao.click()
sleep(2)
botao = driver.find_element_by_class_name("mat-option-text")
botao.click()
sleep(5)
html = driver.page_source
'''
#BAIXANDO DO MINISTERIO DA SAUDE
driver.get(url_ministerio)
botao = driver.find_element_by_class_name("icon-btn")
sleep(2)
botao.click()
sleep(5)
driver.close()

#Renomeando o arquivo
os.chdir(CSV_DIR)
os.system('rm COVID19_ministerio*.csv')
os.system('mv *COVID19_*.csv COVID19_ministerio_' + data_hoje + '.csv')

#BAIXANDO wcota
arquivo = requests.get(url_wcota_cidades)
open(CSV_DIR + 'cidades.tempo.csv', 'wb').write(arquivo.content)
arquivo = requests.get(url_wcota_gps)
open(CSV_DIR + 'cidades.gps.csv', 'wb').write(arquivo.content)
'''
#Conversao pra CSV
soup = BeautifulSoup(html, 'lxml')
tabela = soup.find_all("table")

rows = []
header = ['data','cidade','confirmado','suspeitos','obitos']
rows.append(header)

for row in tabela[0].find_all('tr'):
    colunas = row.find_all('td')
    cols = [data_hoje]
    for coluna in colunas:
        cols.append(coluna.get_text())
    rows.append(cols)
del rows[1]

with open('sec-ce-' + data_hoje +'.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)
