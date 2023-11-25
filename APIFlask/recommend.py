import os
import json
import pickle
from flask import Flask, jsonify, request

# flask --app recommend.py run --port 32194 
# wget --header='Content-Type: application/json' --post-data '{"songs": ["Yesterday", "Bohemian Rhapsody"]}' http://127.0.0.1:32194/api/recommend/ -q -O -

app = Flask(__name__)

# app.model = pickle.load(open(model_path, "rb")) Initialized once
# app.last_modified = os.path.getmtime(model_path)

@app.route('/')
def error():
    return "<p> 404 Not Found! Try /api/recommend/.</p>"

# playlist_ids, version, model_date
@app.route('/api/recommend/', methods=["POST"])
def index():
    #x = os.path.getmtime(model_path(model.picle))
    #if x != app.last_modified = pickle.load and app.last_modified = x  #Reinitialized again
    
    req = request.get_json(force=True)
    print(req, req['songs']) # Gets the list of songs.
    #Temporary return.
    return jsonify({'song': 'hi',
                    'author': 'world'})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 32194))
    app.run(host='0.0.0.0', port=port)
