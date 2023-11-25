import pickle
import math

def playlist_recommender(musics, qtd):
  
  # Número de musicas para cada musica 
  n_per_music = math.ceil(qtd/len(musics))
  print(len(musics))

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
