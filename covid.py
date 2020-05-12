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
import pandas as pd

#Fonte: Ministério da Saúde

CSV_DIR = '/dados/flask/cimai/covid/'

today = date.today()
data_hoje = today.strftime("%Y-%m-%d")

url = 'https://covid.saude.gov.br/'

#OPCOES
options = Options()
options.headless = True
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", CSV_DIR)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;text/csv")

os.chdir(CSV_DIR)
os.system('rm -f DT_PAINEL*.xlsx')

#abrindo o navegador
print("Abrindo o navegador...")
driver = webdriver.Firefox(options=options,firefox_profile=profile)

#BAIXANDO DO MINISTERIO DA SAUDE
os.system('rm -f DT_PAINEL*.xlsx')
driver.get(url)
sleep(3)
botao = driver.find_element_by_css_selector("div.no-shadow:nth-child(2) > ion-button:nth-child(1)")
sleep(2)
botao.click()
sleep(5)
driver.quit()
print("Arquivo salvo com sucesso! Fechando navegador!")
#Renomeando o arquivo
os.system('mv DT_PAINEL*.xlsx cidades.brasil.hoje.xlsx')
print("Convertendo arquivo...")
df = pd.read_excel(CSV_DIR + 'cidades.brasil.hoje.xlsx')
df.to_csv(CSV_DIR + 'cidades.brasil.hoje.csv',index=False,header=True)
print("FINALIZADO COM SUCESSO!")