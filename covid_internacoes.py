# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from time import sleep
import time
from datetime import date

#Fonte: Secretaria de Saúde/CE
CSV_DIR = '/dados/www/html/covid_csv/spyder/'

url = 'https://indicadores.integrasus.saude.ce.gov.br/indicadores/indicadores-coronavirus/historico-internacoes-covid?modoExibicao=painel'

def aguardaAparecerCarregando(driver,delay):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, 'app-loading')))
    except TimeoutException:
        print ("FALHOU! NÃO apareceu o carregando!")

def aguardaDesaparecerCarregando(driver,delay):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'app-loading')))
    except TimeoutException:
        print ("FALHOU! NÃO sumiu o carregando")

def getHTML(diaInicial=1,mes='03',headless=False,hoje=True,linhas=[],colunas=[],maxDia=31,anterior=True):

    today = date.today()
    data_hoje = today.strftime("%Y-%m-%d")
    #abrindo o navegador
    options = Options()
    options.headless = headless
    driver = webdriver.Firefox(options=options)
    #BAIXANDO DA SECRETARIA DA SAUDE/CE
    driver.get(url)
    sleep(8)
    cidades = [2,8,11,17,20,21,24,26,32,34,39,52,58,64,96,97,99,101,109,111,114,122,138,145,146,157,160,171,183]
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    if (hoje): #Baixa apenas a tabela do dia
        botao = driver.find_element_by_css_selector("#mat-select-0 > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)")
        botao.click()
        sleep(4)
        for cidade in cidades:
            botao = driver.find_element_by_css_selector("#mat-option-" + str(cidade) + " > mat-pseudo-checkbox:nth-child(1)")
            botao.click()
            sleep(4)
        '''
        botao = driver.find_element_by_css_selector("#mat-option-52 > mat-pseudo-checkbox:nth-child(1)")
        botao.click()
        sleep(4)
        botao = driver.find_element_by_css_selector("#mat-option-99 > mat-pseudo-checkbox:nth-child(1)")
        botao.click()
        sleep(4)
        botao = driver.find_element_by_css_selector("#mat-option-24 > mat-pseudo-checkbox:nth-child(1)")
        botao.click()
        sleep(4)
        '''
        html = driver.page_source
        with open(CSV_DIR + 'sec-ce-internacoes-hoje.html', 'w') as arquivo:
            arquivo.write(html)
            arquivo.close()
    #Finalizando
    driver.quit()

dia_hoje = int(date.today().strftime("%d"))
print("Baixando HOJE")
getHTML(headless=True,hoje=True)
