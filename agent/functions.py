import numpy as np
import math
import yfinance as yfin
from pandas_datareader import data as pdr

# Stock Market Data Preprocessing

# Definiremos algumas funções uteis

# Sigmoid
def sigmoid(x):
  return 1 / (1 + math.exp(-x))

# Função para formatar texto
def stock_price_format(n):
  if n < 0:
    return "- # {0:2f}".format(abs(n))
  else:
    return "$ {0:2f}".format(abs(n))

# Busca dados no Yahoo Finance
# Formato data = "yyyy-mm-dd"
def dataset_loader(stock_name, initial_date, final_date):

  yfin.pdr_override()

  dataset = pdr.get_data_yahoo(stock_name, start=initial_date, end=final_date)
  
  start_date = str(dataset.index[0]).split()[0]
  end_date = str(dataset.index[1]).split()[0]
  
  close = dataset['Close']
  
  return close