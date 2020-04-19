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
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

#abrindo o navegador
driver = webdriver.Firefox(options=options,firefox_profile=profile)

#BAIXANDO DO MINISTERIO DA SAUDE
driver.get(url)
sleep(3)
botao = driver.find_element_by_css_selector(".btn-outline")
sleep(2)
botao.click()
sleep(5)
driver.quit()

#Renomeando o arquivo
os.chdir(CSV_DIR)
os.system('rm -f cidades.brasil.hoje.csv')
os.system('mv *COVID19_*.csv cidades.brasil.hoje.csv')
