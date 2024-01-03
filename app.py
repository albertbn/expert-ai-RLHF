import os
import pandas as pd
from bs4 import BeautifulSoup
from typing import Union
from json import dumps, loads
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from Data import Data, COL_DID, COL_OPTION_ORDER
from utils.db import df_to_sql
from Ai import extract_ads_features, create_list_new_ads

from dotenv import load_dotenv
load_dotenv()

# TOPIC = 'iran-united-states-hormuz'
TOPIC = 'russia-ukraine-war-influence-energy'
# COOKIE_NAME = 'dids_used'
COOKIE_NAME = f"dids_used_{TOPIC.replace('-', '_')}"

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
        if not params:
            params = {'data': [], 'dids': dumps([]), 'options_order': dumps([]), 'cookie_name': COOKIE_NAME}
        else:
            dids = [o.get(COL_DID) for o in params]
            options_order = [o.get(COL_OPTION_ORDER) for o in params]
            params = {'data': params, 'dids': dumps(dids),
                      'options_order': dumps(options_order), 'cookie_name': COOKIE_NAME}

    return render_template('index.html', **params)


@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    results = data['results']
    dids = data['dids']

    client_ip = request.remote_addr

    # print(results, dids)
    df = pd.DataFrame({COL_DID: dids,
                       'category': [''] * len(results),
                       'paragraph1': results,
                       'paragraph2': results,
                       'metadata': [{}] * len(results),
                       'topic': [TOPIC] * len(results)
                       })
    df['paragraph1'] ^= 1
    df['paragraph2'] &= 1
    # Update the 'metadata.ip' field in the DataFrame with the client's IP address
    df['metadata'] = df['metadata'].apply(lambda x: {**x, 'ip': client_ip})
    df['metadata'] = df['metadata'].apply(lambda x: dumps(x))

    df_to_sql(df)

    return jsonify({'status': 'success'})


def get_dids_from_cook() -> Union[None, list[int]]:
    dids_used = request.cookies.get(COOKIE_NAME)
    return loads(dids_used) if dids_used else None


# region fad knocker
@app.route('/fad_knocker', methods=['POST'])
def fad_knocker():
    # TODO - get here: full_html, image (already here), visual_banners_markup: list[str]
    data = request.json
    print(f'fed_knocker data:: {data}')
    base64_image = data['image']

    full_html = data['full_html']
    soup = BeautifulSoup(full_html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    full_article_text = soup.get_text()

    ads_features = extract_ads_features(base64_image)
    new_ads_list = create_list_new_ads(ads_features, full_article_text)
    return jsonify({'status': 'success', 'ads_features': ads_features, 'new_ads_list': new_ads_list})
# endregion fad knocker


if __name__ == '__main__':
    app.run(host=flask_server_config['host'], port=flask_server_config['port'], debug=flask_server_config['debug'],
            threaded=flask_server_config['threaded'])
