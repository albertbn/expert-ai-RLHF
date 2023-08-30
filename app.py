import os
from typing import Union
from json import dumps, loads
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from Data import Data, COL_DID, COL_OPTION_ORDER

from dotenv import load_dotenv

load_dotenv()

flask_server_config = {

    'host': '0.0.0.0',
    'port': int(os.getenv('PORT', 5000)),
    'debug': True,
    'threaded': True
}

app = Flask(__name__)
CORS(app)

POST = 'POST'


@app.route('/', methods=('GET', POST))
def index():
    with Data() as obj:
        params = obj.get_pairs(exclude_indices=get_dids_from_cook())
        dids = [o.get(COL_DID) for o in params]
        options_order = [o.get(COL_OPTION_ORDER) for o in params]
        params = {'data': params, 'dids': dumps(dids), 'options_order': dumps(options_order)}

    return render_template('index.html', **params)

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    category = data['category']
    paragraph = data['paragraph']

    # conn = sqlite3.connect('votes.db')
    # c = conn.cursor()
    # c.execute("INSERT INTO votes (category, paragraph) VALUES (?, ?)", (category, paragraph))
    # conn.commit()
    # conn.close()

    return jsonify({'status': 'success'})

def get_dids_from_cook() -> Union[None, list[int]]:
    dids_used = request.cookies.get('dids_used')
    return loads(dids_used) if dids_used else None

if __name__ == '__main__':
    app.run(host=flask_server_config['host'], port=flask_server_config['port'], debug=flask_server_config['debug'],
            threaded=flask_server_config['threaded'])
