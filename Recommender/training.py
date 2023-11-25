import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import *
import os
import pickle


dir = "dataset/2023_spotify_ds1.csv"
model_path = './model/'

# Carregando dataset
def Load_Database(dir):
  DF = pd.read_csv(dir)
  return DF

def Model_train(dir):
    DF = Load_Database(dir)
    df_onehot = DF.groupby(['pid', 'track_name'])['track_name'].count().unstack().fillna(0)
    
    def encode_units(x):
        if x <= 0:
            return False
        if x >= 1:
            return True
    
    df_onehot = df_onehot.applymap(encode_units)
    frequent_itemsets = apriori(df_onehot, min_support = 0.04, use_colnames = True, verbose = 1)
    
    rules = association_rules(frequent_itemsets, metric = "lift", min_threshold=1)
    
    print(rules.shape)
    
    # se não houver o diretorio ou o arquivo pickle, criar um
    # if not os.path.exists("{model_path}"):
    #     os.makedirs("{model_path}")
    
    # Gerando o conjunto de regras
    rules.to_pickle(f"{model_path}rules.pkl")
