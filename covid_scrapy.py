# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from time import sleep
from datetime import date

#Fonte: Secretaria de Saúde/CE

CSV_DIR = '/dados/www/html/covid_csv/'

today = date.today()
data_hoje = today.strftime("%Y-%m-%d")

url = 'https://indicadores.integrasus.saude.ce.gov.br/indicadores/indicadores-coronavirus/coronavirus-ceara'

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

with open(CSV_DIR + 'sec-ce-' + data_hoje +'.html', 'w') as arquivo:
    arquivo.write(html)
    arquivo.close()
