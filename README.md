# covid19
<h1>DATASETS COVID19 - BRASIL, CEARÁ E CARIRI</h1>
<h4>Cron dos arquivos deste projeto: 56 11,19,23 * * * (todos os dias, no minuto 56, nas horas 11,19 e 23) </h4>
<h4>Cron dos bots: 40 10,17,23 * * * (todos os dias, no minuto 40, nas horas 10,17 e 23)</h4>
<ul>
 <li><b>agendamento.sh</b>: Script de agendamento para baixar datasets</li>
 <li><b>cidadeGPS.txt</b>: dicionário (python) com os municipios do ceara e a respectiva coordenada</li>
 <li><b>cidadeID.txt</b>: dicionário (python) com os municipios do ceara e os respectivos ids</li>
 <li><b>cidades.brasil.hoje.csv</b>: Dataset do <a href="https://covid.saude.gov.br/">ministério da saúde</a> </li>
 <li><b>cidades.cariri.completo.csv</b>: Dataset das 29 cidades do cariri, com id_ibge, cidade,latitude e longitude</li>
 <li><b>cidades.ceara.completo.csv</b>: Dataset das cidades do ceará, com id_ibge, cidade,latitude e longitude</li>
 <li><b>cidades.brasil.completo.csv</b>: Dataset das cidades do brasil, com id_ibge, cidade,latitude e longitude</li>
 <li><b>covid.ceara.csv</b>: Dataset bruto da secretaria de saude/ce
 <li><b>covid_ceara/ </b>: Projeto Scrapy que gera o arquivo TODOS.CEARA.HOJE.CSV a partir dos dados baixados por agendamento.sh</li>
 <li><b>covid.py </b>: Bot que baixa os dados do ministério da saúde</li>
 <li><b>covid_scrapy.py </b>: Bot que baixa os dados da secretaria de saúde do ceará</li>
 <li><b>covid.sqlite3 </b>: Banco de dados (ainda em desenvolvimento)</li>
 <li><b>municipios.csv</b>: Lista de municipios do brasil</li>
 <li><b>time.txt </b>: Data e hora da última atualização dos bots</li>
 <li><b>todos.cariri.hoje.csv </b>: filtro de TODOS.CEARA.HOJE.CSV para as cidades do cariri</li>
 <li><b>TODOS.CEARA.HOJE.CSV </b>: Dataset baixado e processado pelos procedimentos em agendamento.sh</li>

</ul>
