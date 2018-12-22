import time

from flask import Flask, request
from flask_cors import CORS
from sqlalchemy import desc

from settings import ENV
from models import VideoEntry, db

from utils import add_headers

app = Flask(__name__)
CORS(app)

app.config.from_object(ENV)
db.init_app(app)


def insert_one(vid):
    now = time.time()
    vid.created = now
    vid.last_checked = now
    db.session.add(vid)
    db.session.commit()


@app.route("/videos", methods=['GET'])
def get_by_title():
    if 'key' in request.args:
        key = request.args.get('key')
        matches = db.session.query(VideoEntry).filter(VideoEntry.title.like("%" + key + "%")).all()
    elif 'from_id' in request.args and 'to_id' in request.args:
        from_id = request.args.get('from_id')
        to_id = request.args.get('to_id')
        matches = db.session.query(VideoEntry).filter(from_id <= VideoEntry.id).filter(VideoEntry.id <= to_id)
    else:
        return add_headers({'result': 'Error in url args'}, 400)
    matches = [x.get_json() for x in matches]
    return add_headers(matches, 200)


@app.route("/paginated", methods=['GET'])
def get_paginated():
    category = request.args.get('category') if request.args.get('category') is not None else ""
    key = request.args.get('key') if request.args.get('key') is not None else ""
    page_no = int(request.args.get('page')) if request.args.get('page') is not None else 1
    descend = desc if request.args.get('desc') is not None else lambda *a, **k: None

    matches = db.session.query(VideoEntry) \
        .filter(VideoEntry.title.like("%" + key + "%")) \
        .filter(VideoEntry.title.like("%" + category + "%")) \
        .order_by(descend(VideoEntry.title)) \
        .paginate(page=page_no, per_page=ENV.DEFAULT_PAGESIZE)

    paginated_result = {'elements': list(map(lambda x: x.get_json(), matches.items)), 'pages': matches.pages,
                        'page': matches.page}
    return add_headers(paginated_result, 200)


@app.route("/videos", methods=['POST'])
def add_vid():
    insert_one(VideoEntry(**request.json))
    return add_headers({'result': 'OK'}, 200)


if __name__ == '__main__':
    app.run(host=ENV.HOST, port=ENV.PORT, ssl_context=ENV.SSL_CONTEXT)
