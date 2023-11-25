import os
import json
import time
import pickle
import pandas
from flask import Flask, jsonify, request

# flask --app recommend.py run --port 32194 
# wget --header='Content-Type: application/json' --post-data '{"songs": ["Ride Wit Me", "Red Solo Cup"]}' http://127.0.0.1:32194/api/recommend/ -q -O -
"""
To create a docker container out of this, do:
pipreqs --savepath=requirements.in && pip-compile
docker image build -t flask_docker .
docker run -p 32194:32194 -d flask_docker
"""

# version = "1.0"
version  = os.environ.get('VERSION', 1.0)
model_path = "./model/rules.pkl"

app = Flask(__name__)


import math

def playlist_recommender(musics, qtd = 20):
  
    # Número de musicas para cada musica 
    n_per_music = math.ceil(qtd/len(musics))
    #print(len(musics))

    # Carregando arquivo pickle
    rules = app.model 
    
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

@app.route('/')
def error():
    return "<p> 404 Not Found! Try /api/recommend/.</p>"

# playlist_ids, version, model_date
@app.route('/api/recommend/', methods=["POST"])
def index():

    x = os.path.getmtime(model_path)
    if x != app.last_modified == pickle.load:
        app.model = pickle.load(open(model_path, "rb"))
        app.last_modified = os.path.getmtime(model_path)

    req = request.get_json(force=True)

    print(req, req['songs']) # Gets the list of songs.

    song_list = req['songs']
    song_suggestions = playlist_recommender(song_list)

    print(song_suggestions, version, app.last_modified)

    return jsonify({'songs': list(song_suggestions), 'version': version, 'model_date': app.last_modified})

    #Temporary return.
    #return jsonify({'song': 'hi',
    #                'author': 'world'})

if __name__ == "__main__":
    while not os.path.exists(model_path):
        print("Waiting for pickle.")
        time.sleep(1)

    app.model = pickle.load(open(model_path, "rb"))
    app.last_modified = os.path.getmtime(model_path)

    port = int(os.environ.get('PORT', 32194))
    app.run(host='0.0.0.0', port=port)


