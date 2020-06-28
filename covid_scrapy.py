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

url = 'https://indicadores.integrasus.saude.ce.gov.br/indicadores/indicadores-coronavirus/coronavirus-ceara'

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
    delay = 120
    aguardaAparecerCarregando(driver,delay)
    aguardaDesaparecerCarregando(driver,delay)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    delay = 120
    if (hoje): #Baixa apenas a tabela do dia
        print("Baixando: " + data_hoje)
        try:
            myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, 'mat-select-arrow-wrapper')))
            myElem = WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'app-loading')))
            
        except TimeoutException:
            print ("FALHOU! NÃO CARREGOU ELEMENTO!")
        botao = driver.find_element_by_class_name("mat-select-arrow-wrapper")
        botao.click()
        try:
            myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, 'mat-option-text')))
            
        except TimeoutException:
            print ("FALHOU! NÃO CARREGOU ELEMENTO!")
        botao = driver.find_element_by_class_name("mat-option-text")
        botao.click()
        aguardaAparecerCarregando(driver,delay)
        aguardaDesaparecerCarregando(driver,delay)
        '''
        try:
            myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, 'mat-option-text')))
            
        except TimeoutException:
            print ("FALHOU! NÃO CARREGOU ELEMENTO!")
        '''
        html = driver.page_source
        with open(CSV_DIR + 'sec-ce-' + data_hoje +'.html', 'w') as arquivo:
            arquivo.write(html)
            arquivo.close()
            nomearquivo = CSV_DIR + 'sec-ce-' + data_hoje +'.html'
            print(nomearquivo + " gravado com sucesso...")
    else: #baixa a tabela de um intervalo de dias
        dia = diaInicial
        clicouNoMesAnterior = anterior
        try:
            myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, 'mat-select-arrow-wrapper')))
            myElem = WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'app-loading')))
            
        except TimeoutException:
            print ("FALHOU! NÃO CARREGOU ELEMENTO!")
        botao = driver.find_element_by_class_name("mat-select-arrow-wrapper")
        botao.click()
        try:
            myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, 'mat-option-text')))
            myElem = WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'app-loading')))
            
        except TimeoutException:
            print ("FALHOU! NÃO CARREGOU ELEMENTO: mat-option-text 1")
        botao = driver.find_element_by_class_name("mat-option-text")
        botao.click()
        
        aguardaAparecerCarregando(driver,delay)
        aguardaDesaparecerCarregando(driver,delay)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        
        for i in linhas:
            for j in colunas:
                #Clica no calendario
                try:
                    myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.mat-datepicker-toggle-default-icon')))
                except TimeoutException:
                    print ("FALHOU! NÃO CARREGOU ELEMENTO!")
                driver.find_element_by_css_selector(".mat-datepicker-toggle-default-icon").click()
                #Clica no mês anterior
                if (not clicouNoMesAnterior):
                    try:
                        myElem = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.mat-calendar-previous-button')))
                        
                    except TimeoutException:
                        print ("FALHOU! NÃO CARREGOU ELEMENTO!")
                    driver.find_element_by_css_selector(".mat-calendar-previous-button").click()
                    clicouNoMesAnterior = True
                    
                try:
                    if (dia>maxDia):
                        driver.quit()
                        return
                    #Clica no dia
                    print("Aguardando o dia..." + mes + "-" + '{:02d}'.format(dia))
                    
                    driver.find_element_by_css_selector(".mat-calendar-body > tr:nth-child(" + str(i) + ") > td:nth-child(" + str(j) + ") > div:nth-child(1)").click()
                    aguardaAparecerCarregando(driver,delay)
                    aguardaDesaparecerCarregando(driver,delay)
                    #Monta o nome do arquivo
                    nomearquivo = CSV_DIR + "sec-ce-2020-" + mes + "-" + '{:02d}'.format(dia) + ".html"
                    dia = dia + 1
                    #Processa o conteúdo
                    arquivo = open(nomearquivo,"w")
                    arquivo.write(driver.page_source)
                    arquivo.close()
                    print(nomearquivo + " gravado com sucesso...")
                    if (dia>maxDia):
                        driver.quit()
                        return
                except NoSuchElementException:
                    print("Elemento nao encontrado")
                except ElementClickInterceptedException:
                    print("Erro ElementClick")
                except Exception as e:
                    print(str(e))

    #Finalizando
    driver.quit()

dia_hoje = int(date.today().strftime("%d"))
print("Baixando HOJE")
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
print("Baixando mês de junho de 7 até 30")
getHTML(diaInicial=7,mes="06",headless=True,hoje=False,linhas=range(3,7,1),colunas=range(1,8,1),maxDia=dia_hoje-1,anterior=True)
