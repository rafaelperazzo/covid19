# -*- coding: utf-8 -*-
import sqlalchemy as db

class MyDB:

    def __init__(self, arquivo,tabela):
        self.arquivo = arquivo
        self.tabela = tabela
        self.engine = db.create_engine('sqlite:///' + arquivo)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.tabela = db.Table(tabela, self.metadata, autoload=True, autoload_with=self.engine)

    def getIDFromName(self,cidade):
        consulta = db.select([self.tabela.columns.id]).where(self.tabela.columns.cidade==cidade)
        resultado = self.connection.execute(consulta)
        linhas = resultado.fetchall()
        if (len(linhas)==0):
            return(0)
        else:
            return (int(linhas[0][0]))

    def getGPSFromID(self,id):
        consulta = db.select([self.tabela.columns.gps]).where(self.tabela.columns.id==id)
        resultado = self.connection.execute(consulta)
        linhas = resultado.fetchall()
        if (len(linhas)==0):
            return("0,0")
        else:
            return (str(linhas[0][0]))

    def getPopulacaoFromID(self,id):
        consulta = db.select([self.tabela.columns.populacao]).where(self.tabela.columns.id==id)
        resultado = self.connection.execute(consulta)
        linhas = resultado.fetchall()
        if (len(linhas)==0):
            return(0)
        else:
            return (int(linhas[0][0]))

    def getLatitudeFromID(self,id):
        consulta = db.select([self.tabela.columns.latitude]).where(self.tabela.columns.id==id)
        resultado = self.connection.execute(consulta)
        linhas = resultado.fetchall()
        if (len(linhas)==0):
            return(0)
        else:
            return (float(linhas[0][0]))

    def getLongitudeFromID(self,id):
        consulta = db.select([self.tabela.columns.longitude]).where(self.tabela.columns.id==id)
        resultado = self.connection.execute(consulta)
        linhas = resultado.fetchall()
        if (len(linhas)==0):
            return(0)
        else:
            return (float(linhas[0][0]))

    def close(self):
        self.connection.close()
