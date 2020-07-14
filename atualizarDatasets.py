import pandas as pd

CSV_DIR = '/dados/flask/cimai/covid/'
cariri = ['ABAIARA', 'ALTANEIRA', 'ANTONINA DO NORTE', 'ARARIPE', 'ASSARE', 'AURORA', 'BARBALHA', 'BARRO', 'BREJO SANTO', 'CAMPOS SALES', 'CARIRIACU', 'CRATO', 'FARIAS BRITO', 'GRANJEIRO', 'JARDIM', 'JATI', 'JUAZEIRO DO NORTE', 'LAVRAS DA MANGABEIRA', 'MAURITI', 'MILAGRES', 'MISSAO VELHA', 'NOVA OLINDA', 'PENAFORTE', 'PORTEIRAS', 'POTENGI', 'SALITRE', 'SANTANA DO CARIRI', 'TARRAFAS', 'VARZEA ALEGRE']
df_ceara = pd.read_csv(CSV_DIR + 'TODOS.CEARA.HOJE.CSV',delimiter=",",encoding='utf8',decimal='.')
df_cariri = df_ceara[df_ceara['cidade'].isin(cariri)].sort_values(by=['data','cidade'])
df_ceara.to_csv('/dados/flask/cimai/covid/todos.ceara.hoje.csv',index=False)
df_cariri.to_csv('/dados/flask/cimai/covid/todos.cariri.hoje.csv',index=False)