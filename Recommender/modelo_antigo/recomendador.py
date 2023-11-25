import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import *
import os
import pickle
import math

dir = "datasets/train/2023_spotify_ds1.csv"

model_path = ''
targets_path = ''

# Carregando dataset
def Load_Database(dir):
  DF = pd.read_csv(dir)
  return DF

# Treinando modelo
def Model_train(dir):
    DF = Load_Database(dir)
    # Agrupando playlists pelo pid
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
    if not os.path.exists("{model_path}"):
        os.makedirs("{model_path}")
    
    # Gerando o conjunto de regras
    rules.to_pickle(f"{model_path}rules.pkl")
    # Gerando as playlists targets
    playlists_targets.to_pickle(f"{targets_path}targets.pkl")


# qtd - quantidade de musicas totais na playlist
def playlist_recommender(musics, qtd):
  
  # Número de musicas para cada musica 
  n_per_music = math.ceil(qtd/len(musics))

  # Carregando arquivo pickle
  with open("rules.pkl", 'rb') as rules_pickle:
    rules = pickle.load(rules_pickle)
    
    # Conjunto que será retornado no final
    playlist = set()

    # Para cada musica passada pelo usuário
    for song in musics:
      
      consequents = set()
      
      # Todos os elementos associados a uma musica
      filter_rules = rules[rules['antecedents'].apply(lambda x: song in x)]

      # Todos os consequentes de uma determinada musica
      for consequent in filter_rules['consequents']:
        # A cada iteração coloca todos os consequentes de uma musica em um consjunto
        consequents.update(consequent)
      
      # Transformado em uma lista para facilitar a manipulação
      consequents = list(consequents)
      
      contador = 0
      
      # Para cada musica na lista de consequentes 
      for music in consequents:
        # Contador para inserir uma quantidade x na playlist, a ausencia disso poderia fazer valores
        # duplica entrarem na playlist e não atingir a quantidade total de musicas.
        if contador == n_per_music:
          break
        # Se a musica não estiver na playlist, adicionar
        elif music not in playlist:
          playlist.add(music)
          contador = contador + 1
    
  return playlist