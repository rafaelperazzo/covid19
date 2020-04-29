# -*- coding: utf-8 -*-
from sqlalchemy import create_engine

def atualizarDados(id=0,cidade='indefinida',confirmados=0,suspeitos=0,obitos=0,taxa=0):
    engine = create_engine('sqlite:///dados.cariri.hoje.sqlite3', echo=False)
    conn = engine.connect()
    conn.execute('DROP TABLE IF EXISTS hoje')
    conn.execute('CREATE TABLE hoje (id INT, cidade TEXT, confirmados INT, suspeitos INT, obitos INT, taxa FLOAT)')
    consulta = 'INSERT INTO hoje(id,cidade,confirmados,suspeitos,obitos,taxa) VALUES (?,?,?,?,?,?)'
    conn.execute(consulta,[id,cidade,confirmados,suspeitos,obitos,taxa])
    conn.execute(consulta,[id,cidade,confirmados,suspeitos,obitos,taxa])
    conn.close()

atualizarDados(1111,'JUAZEIRO',2,3,5,0.666)
atualizarDados(2222,'CRATO',2,3,5,0.666)

