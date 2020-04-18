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
from time import sleep
import time
from datetime import date

#Fonte: Secretaria de Saúde/CE
CSV_DIR = '/dados/www/html/covid_csv/spyder/'

url = 'https://indicadores.integrasus.saude.ce.gov.br/indicadores/indicadores-coronavirus/coronavirus-ceara'

def getHTML(diaInicial=1,mes='03',headless=False,hoje=True,linhas=[],colunas=[],maxDia=31,anterior=True):

    today = date.today()
    data_hoje = today.strftime("%Y-%m-%d")
    #abrindo o navegador
    options = Options()
    options.headless = headless
    driver = webdriver.Firefox(options=options)
    #BAIXANDO DA SECRETARIA DA SAUDE/CE
    driver.get(url)
    sleep(3)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    sleep(2)
    if (hoje): #Baixa apenas a tabela do dia
        botao = driver.find_element_by_class_name("mat-select-arrow-wrapper")
        botao.click()
        sleep(2)
        botao = driver.find_element_by_class_name("mat-option-text")
        botao.click()
        sleep(3)
        html = driver.page_source
        with open(CSV_DIR + 'sec-ce-' + data_hoje +'.html', 'w') as arquivo:
            arquivo.write(html)
            arquivo.close()
    else: #baixa a tabela de um intervalo de dias
        dia = diaInicial
        clicouNoMesAnterior = anterior
        botao = driver.find_element_by_class_name("mat-select-arrow-wrapper")
        botao.click()
        sleep(2)
        botao = driver.find_element_by_class_name("mat-option-text")
        botao.click()
        sleep(2)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        sleep(1)
        for i in linhas:
            for j in colunas:
                #Clica no calendario
                driver.find_element_by_css_selector(".mat-datepicker-toggle-default-icon").click()
                sleep(2)
                #Clica no mês anterior
                if (not clicouNoMesAnterior):
                    driver.find_element_by_css_selector(".mat-calendar-previous-button").click()
                    clicouNoMesAnterior = True
                    sleep(2)

                try:
                    if (dia>maxDia):
                        driver.quit()
                        return
                    #Clica no dia
                    driver.find_element_by_css_selector(".mat-calendar-body > tr:nth-child(" + str(i) + ") > td:nth-child(" + str(j) + ") > div:nth-child(1)").click()
                    sleep(2)
                    #Monta o nome do arquivo
                    nomearquivo = CSV_DIR + "sec-ce-2020-" + mes + "-" + '{:02d}'.format(dia) + ".html"
                    dia = dia + 1
                    #Processa o conteúdo
                    arquivo = open(nomearquivo,"w")
                    arquivo.write(driver.page_source)
                    arquivo.close()
                    print(nomearquivo + " gravado com sucesso...")
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
print("Baixando MES ABRIL ATE DIA 04")
getHTML(diaInicial=1,mes="04",headless=True,hoje=False,linhas=range(1,2,1),colunas=range(2,6,1),maxDia=4,anterior=True)
print("Baixando MES ABRIL DE 05 A " + str(dia_hoje))
getHTML(diaInicial=5,mes="04",headless=True,hoje=False,linhas=range(2,6,1),colunas=range(1,8,1),maxDia=dia_hoje,anterior=True)
