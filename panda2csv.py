
import pandas as pd
DIR = '/dados/flask/cimai/covid/'
df = pd.read_json(DIR + 'covid.ceara.json')
df.to_csv(DIR + 'covid.ceara.csv',index=False)
