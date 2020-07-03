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
import logging

#Fonte: Secretaria de Saúde/CE
CSV_DIR = '/dados/www/html/covid_csv/spyder/'
logging.basicConfig(filename=CSV_DIR + 'covid.scrapy.log', filemode='w', format='%(asctime)s %(name)s - %(levelname)s - %(message)s',level=logging.ERROR)
url = 'https://indicadores.integrasus.saude.ce.gov.br/indicadores/indicadores-coronavirus/coronavirus-ceara'

def aguardaAparecerCarregando(driver,delay):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME, 'app-loading')))
    except TimeoutException:
        logging.error("Nao apareceu o app-loading...")

def aguardaDesaparecerCarregando(driver,delay):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'app-loading')))
    except TimeoutException:
        logging.error("Nao desapareceu o app-loading...")

def getHTML(diaInicial=1,mes='03',headless=False,hoje=True,linhas=[],colunas=[],maxDia=31,anterior=True):

    today = date.today()
    data_hoje = today.strftime("%Y-%m-%d")
    #abrindo o navegador
    options = Options()
    options.headless = headless
    driver = webdriver.Firefox(options=options)
    #BAIXANDO DA SECRETARIA DA SAUDE/CE
    driver.get(url)
    delay = 120
    aguardaAparecerCarregando(driver,delay)
    aguardaDesaparecerCarregando(driver,delay)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    if (hoje): #Baixa apenas a tabela do dia
        print("Baixando: " + data_hoje)
        try:
            myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, 'mat-select-arrow-wrapper')))
            myElem = WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'app-loading')))
            
        except TimeoutException:
            logging.error ("FALHOU! NÃO CARREGOU ELEMENTO!")
        botao = driver.find_element_by_class_name("mat-select-arrow-wrapper")
        botao.click()
        try:
            myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, 'mat-option-text')))
            
        except TimeoutException:
            logging.error("Nao carregou elemento..")
        botao = driver.find_element_by_class_name("mat-option-text")
        continuar = True
        while (continuar):
            try:
                botao.click()
                continuar = False
            except ElementClickInterceptedException:
                logging.error("Erro ao clicar, tentando novamente...")
        #botao.click()
        aguardaAparecerCarregando(driver,delay)
        aguardaDesaparecerCarregando(driver,delay)
        
        html = driver.page_source
        with open(CSV_DIR + 'sec-ce-' + data_hoje +'.html', 'w') as arquivo:
            arquivo.write(html)
            arquivo.close()
            nomearquivo = CSV_DIR + 'sec-ce-' + data_hoje +'.html'
            logging.debug(nomearquivo + " gravado com sucesso...(HOJE)")
    else: #baixa a tabela de um intervalo de dias
        dia = diaInicial
        clicouNoMesAnterior = anterior
        try:
            myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, 'mat-select-arrow-wrapper')))
            myElem = WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'app-loading')))
            
        except TimeoutException:
            logging.error("Clicando nas situacoes...")
        botao = driver.find_element_by_class_name("mat-select-arrow-wrapper")
        botao.click()
        try:
            myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, 'mat-option-text')))
            myElem = WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'app-loading')))
            
        except TimeoutException:
            logging.error("Clicando em TODOS")
        botao = driver.find_element_by_class_name("mat-option-text")
        botao.click()
        
        aguardaAparecerCarregando(driver,delay)
        aguardaDesaparecerCarregando(driver,delay)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        
        for i in linhas:
            for j in colunas:
                #Clica no calendario
                try:
                    myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'mat-form-field.mat-form-field:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)')))
                except TimeoutException:
                    logging.error("Clicar no calendario...")
                logging.debug("Clicando no calendario...")
                driver.find_element_by_css_selector("mat-form-field.mat-form-field:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)").click()
                
                #Clica no mês anterior
                if (not clicouNoMesAnterior):
                    try:
                        myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.mat-calendar-previous-button')))
                        
                    except TimeoutException:
                        logging.error("Mes anterior...")
                    logging.debug("Clicando no mes anterior...")
                    driver.find_element_by_css_selector("button.mat-focus-indicator:nth-child(3)").click()
                    clicouNoMesAnterior = True
                    
                try:
                    if (dia>maxDia):
                        driver.quit()
                        return
                    #Clica no dia
                    logging.debug("Aguardando o dia..." + mes + "-" + '{:02d}'.format(dia))
                    continuar = True
                    while (continuar):
                        try:
                            driver.find_element_by_css_selector(".mat-calendar-body > tr:nth-child(" + str(i) + ") > td:nth-child(" + str(j) + ") > div:nth-child(1)").click()
                            continuar = False
                        except(ElementClickInterceptedException):
                            logging.error("Erro ao clicar no dia: " + str(dia))
                    aguardaAparecerCarregando(driver,delay)
                    aguardaDesaparecerCarregando(driver,delay)
                    #Monta o nome do arquivo
                    nomearquivo = CSV_DIR + "sec-ce-2020-" + mes + "-" + '{:02d}'.format(dia) + ".html"
                    dia = dia + 1
                    #Processa o conteúdo
                    arquivo = open(nomearquivo,"w")
                    arquivo.write(driver.page_source)
                    arquivo.close()
                    logging.debug(nomearquivo + " gravado com sucesso...")
                    if (dia>maxDia):
                        driver.quit()
                        return
                except NoSuchElementException:
                    logging.error("Elemento nao encontrado")
                except ElementClickInterceptedException:
                    logging.error("Erro ElementClick")
                except Exception as e:
                    logging.error(str(e))

    #Finalizando
    logging.debug("Finalizando...")
    driver.quit()

dia_hoje = int(date.today().strftime("%d"))
logging.debug("Baixando HOJE")
getHTML(headless=True,hoje=True)
#print("Baixando MES MARCO")
#getHTML(diaInicial=1,mes="03",headless=True,hoje=False,linhas=range(2,7,1),colunas=range(1,8,1),maxDia=31,anterior=False)
#print("Baixando MES ABRIL ATE DIA 04")
#getHTML(diaInicial=1,mes="04",headless=True,hoje=False,linhas=range(1,2,1),colunas=range(2,6,1),maxDia=4,anterior=False)
#print("Baixando MES ABRIL DE 05 A 30")
#getHTML(diaInicial=5,mes="04",headless=True,hoje=False,linhas=range(2,6,1),colunas=range(1,8,1),maxDia=30,anterior=False)
#print("Baixando mês de maio de 1 a 2")
#getHTML(diaInicial=1,mes="05",headless=True,hoje=False,linhas=range(1,2,1),colunas=range(2,4,1),maxDia=2,anterior=True)

#print("Baixando mês de maio de 3 a 31")
#getHTML(diaInicial=3,mes="05",headless=False,hoje=False,linhas=range(2,7,1),colunas=range(1,8,1),maxDia=31,anterior=False)

#print("Baixando mês de junho de 1 até 6")
#getHTML(diaInicial=1,mes="06",headless=False,hoje=False,linhas=range(2,7,1),colunas=range(2,8,1),maxDia=6,anterior=True)

#print("Baixando mês de julho de 1 até 4")
#getHTML(diaInicial=1,mes="07",headless=True,hoje=False,linhas=range(1,2,1),colunas=range(2,6,1),maxDia=dia_hoje-1,anterior=True)

#print("Baixando mês de junho de 7 até 30")
#getHTML(diaInicial=7,mes="06",headless=True,hoje=False,linhas=range(3,7,1),colunas=range(1,8,1),maxDia=30,anterior=False)


