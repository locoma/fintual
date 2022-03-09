# -*- coding: utf-8 -*-
"""

@author: Matias Mayer
"""
#intente dejar el path estandar con __file__ pero en sypder no funciona
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

def date_subset(data,date1,date2,column):
    """Cambiamos formato fecha a uno amigable"""
    date_inf1=pd.to_datetime(date1,format="%d/%m/%Y")
    date_sup1=pd.to_datetime(date2,format="%d/%m/%Y")
    data[column]=pd.to_datetime(data[column],format="%d/%m/%Y")
    """Tomo el subconjunto con el input que me dieron"""
    data=data[(data[column]>date_inf1) & (data[column]<date_sup1)]
    """Reseteo lo indices de la tabla y luego dejo la fecha como indice, esto para ocupar las funciones de calculo"""
    data=data.reset_index(drop=True)
    data=data.set_index(column)
    return data

def total_months(date1,date2):
    """Calculo el N para luego anualizar el retorno del portafolio"""
    date_inf1=pd.to_datetime(date1,format="%d/%m/%Y")
    date_sup1=pd.to_datetime(date2,format="%d/%m/%Y")
    N=date_sup1-date_inf1
    N = (np.round(pd.to_numeric(N.days)/365))*12
    return N

""" portafolio returns"""
def port_returns(n,data):
    weight=np.repeat(1/n,n)
    daily_ret=data.pct_change()
    port_ret=daily_ret.mul(weight,axis=1).sum(axis=1)
    return port_ret

"""calculo el retorno anualizado"""
def annual_port_ret(n,data,n_stocks):
    weight=np.repeat(1/n_stocks,n_stocks)
    port_price=data.mul(weight,axis=1).sum(axis=1)
    port_ret_f=(port_price[-1]-port_price[0])/port_price[0]
    annual_ret=((1+port_ret_f)**(12/n))-1
    return annual_ret
"""Ahora empieza la metodología para calcular los retornos del portafolio"""
#pesos del portafolio, para este caso EW, si no se asignarian de tal manera que sumen uno dejo ejemplo
#weight=np.array([0.2,0.1,0.5,0.05,0.15])
""" en base al numero de stock, calcula los pesos que son iguales para este caso"""

path=str(input("Ingresa el path donde esten los datos a utilizar sin comillas(C:/ruta/file.csv) "))
#podemos parsear las fechas en caso de errores de formato por eso me aseguro despues que esten en el formato que quiero
""" Leemos la base"""
stock_price=pd.read_csv(path)
"""Recibimos inputs para rangos fechas """
#ES IMPORTANTE QUE ASUMO QUE LA BASE ESTA EN BUEN FORMATO, SINO HABRIA QUE UTILIZAR COMANDOS PARA ARREGLAR LA FECHA
date_inf=input("Ingrese fecha inicial formato day/month/year(minimo 14/04/2015, maximo 09/04/2020 ) ")
date_sup=input("Ingrese fecha superior formato day/month/year(minimo 14/04/2015,maximo 09/04/2020 ) ")
number_stocks=5
"""arreglamos formato y sacamos el subset de interes"""
stock_price_f=date_subset(stock_price,date_inf,date_sup,"Date")

"""calculamos retornos"""
portfolio_returns=port_returns(number_stocks,stock_price_f)
print(portfolio_returns)

""" calculo tiempo para anualizar, se ocupa en la ultima función"""
months=total_months(date_inf,date_sup)

"""portafolio returns anualizados"""
annual_port_returns=annual_port_ret(months,stock_price_f,number_stocks)
print(annual_port_returns)

