from flask import Flask, request
from flask_cors import CORS

import entry_repo as db
from entry import VideoEntry
from settings import PORT, HOST
from utils import add_headers

app = Flask(__name__)
CORS(app)


@app.route("/videos", methods=['GET'])
def get_by_title():
    if 'key' in request.args:
        key = request.args.get('key')
        matches = db.get_by_title(key)
    elif 'from_id' in request.args and 'to_id' in request.args:
        from_id = request.args.get('from_id')
        to_id = request.args.get('to_id')
        matches = db.get_range(from_id, to_id)
    else:
        return add_headers({'result': 'Error in url args'}, 400)
    matches = [x.get_json() for x in matches]
    return add_headers(matches, 200)


@app.route("/videos", methods=['POST'])
def add_vid():
    db.insert_one(VideoEntry(**request.json))
    return add_headers({'result': 'OK'}, 200)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
