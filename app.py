# from datetime import datetime
import os
from json import dumps
# import traceback
# import logging
from werkzeug.datastructures import ImmutableMultiDict
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from urllib.parse import unquote
from Data import Data, COL_DID

from dotenv import load_dotenv

load_dotenv()

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.INFO)

flask_server_config = {

    'host': '0.0.0.0',
    'port': int(os.getenv('PORT', 5000)),
    # 'debug': False,
    'debug': True,
    'threaded': True
}

app = Flask(__name__)
# app.secret_key = os.urandom(12)
CORS(app)

POST = 'POST'


@app.route('/files/<path:path>')
def files(path):
    """
    A route for files
    @param path:
    @return:
    """
    return send_from_directory('files', path)


def params_json() -> dict:
    params = request.get_json() if request is not None else None
    if not params:
        params = request.form.to_dict()
    if not params:
        params = request.args
        if params:
            params = params.to_dict()

    return params


# @app.route('/api', methods=('GET', POST))
# def api_call():
#     status_code = 200
#     params = params_json()
#     if params is None:
#         result = {'error': 'no command'}
#         status_code = 404
#     else:
#         params['query'] = unquote(params.get('query'))
#         result = api.get_top_n_search_results(**params)
#
#     response = jsonify(result)
#     response.status_code = status_code
#     return response

@app.route('/', methods=('GET', POST))
def index():
    # if request.method == POST:
    #     params: dict = get_form_params(request.form)
    #     search_results = api.get_top_n_search_results(**params)
    #     params.update(search_results)
    #     return render_template('index.html', **params)
    with Data() as obj:
        params = obj.get_pairs()
        dids = [o.get(COL_DID) for o in params]
        params = {'data': params, 'dids': dumps(dids)}

    return render_template('index.html', **params)


def get_form_params(req: ImmutableMultiDict) -> dict:
    ret = {
        'query': unquote(req.get('query', '')),
        'top_n': int(req.get('engine_id', 10))
    }
    return ret


if __name__ == '__main__':
    app.run(host=flask_server_config['host'], port=flask_server_config['port'], debug=flask_server_config['debug'],
            threaded=flask_server_config['threaded'])
