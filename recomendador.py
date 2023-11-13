import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import *
import os
import pickle
import random

dir = "datasets/train/2023_spotify_ds1.csv"

def Load_Database(dir):
  DF = pd.read_csv(dir)
  return DF

def Model_train(dir):
    DF = Load_Database(dir)
    df_onehot = DF.groupby(['pid', 'track_name'])['track_name'].count().unstack().fillna(0)
    playlists_targets = DF.groupby('pid')['track_name'].apply(list)
    
    def encode_units(x):
        if x <= 0:
            return False
        if x >= 1:
            return True
    
    df_onehot = df_onehot.applymap(encode_units)
    frequent_itemsets = apriori(df_onehot, min_support = 0.05, use_colnames = True, verbose = 1)
    
    rules = association_rules(frequent_itemsets, metric = "lift", min_threshold=1)
    
    # se não houver o diretorio ou o arquivo pickle, criar um
    if not os.path.exists("/app/models"):
        os.makedirs("/app/models")
    
    # Gerando o conjunto de regras
    rules.to_pickle(f"/app/models/rules.pkl")
    # Gerando as playlists targets
    playlists_targets.to_pickle(f"/app/models/targets.pkl")
  
def playlist_recommender(musics):
    with open("/app/models/rules.pkl", 'rb') as rules_pickle, open("/app/models/targets.pkl", 'rb') as playlists_pickle:
        # instanciando o arquivo pickle
        rules = pickle.load(rules_pickle)
        playlists = pickle.load(playlists_pickle)
            
        validator = False
        # percorrendo o dataframe
        for i in range(len(list(rules['antecedents']))):
            # encontrar o conjunto de musicas em antecedentes
            if(set(musics).issubset(list(rules['antecedents'][i]))):
                # salvando a posição do primeiro match no dataframe
                validator = True
                value = i
                # incluir um valor aleatorio caso não encontre nenhuma combinação.
                break
            else:
                n_antecedents = i
        
        if(validator == False):
            # Retornando uma playlist aleatoria caso a combinação de musicas do usuário não seja compativel 
            value = random.randint(0, n_antecedents)
        
        # pegando a linha dos valores consquentes
        consequents = rules.iloc[value]

        # Para o conjunto de musicas passados, pegar os comuns e salvar em formato de array
        common_musics = list(consequents['consequents'])

        # dicionario com o pid como chave e musicas como valores
        for i in range(len(playlists)):
            # Se as musicas encontradas atraves do match estiver em alguma das playlists, retornar a playlist
            if(set(common_musics).issubset(playlists.iloc[i])):
                print(playlists.keys()[i])
                print(playlists.iloc[i])
                break