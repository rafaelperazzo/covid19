# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

HTML_DIR = "/dados/www/html/covid_csv/spyder/"

soup = BeautifulSoup(open(HTML_DIR + "sec-ce-comorbidades-hoje.html"),'lxml')

obitos_comorbidade = soup.find_all('text',attrs={'class':'value-text'})[5].get_text()
obitos_comorbidade = obitos_comorbidade.lstrip()
obitos_comorbidade = obitos_comorbidade.rstrip()
print(obitos_comorbidade)

obitos_por_dia = soup.find_all('text',attrs={'class':'value-text'})[3].get_text()
obitos_por_dia = obitos_por_dia.lstrip()
obitos_por_dia = obitos_por_dia.rstrip()
print(obitos_por_dia)

