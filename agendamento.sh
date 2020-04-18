#Baixando dataset bruto da secretaria de estado-ce
/usr/bin/wget -O /dados/www/html/covid_csv/covid.ceara.csv https://indicadores.integrasus.saude.ce.gov.br/api/casos-coronavirus/export-csv
#Baixando paginas dia a dia
/usr/bin/python3 /dados/flask/cimai/covid/covid_scrapy.py
#Executando o scrapy
cd /dados/flask/cimai/covid/covid_ceara/covid_ceara/
/usr/local/bin/scrapy crawl Todos 
#Atualizar datasets
/usr/bin/curl "https://apps.yoko.pet/cimai/atualizaDatasets"
#Gravar hora
/bin/date '+%d/%m/%Y %H:%M:%S' > /dados/flask/cimai/covid/time.txt
