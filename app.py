import time

from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from settings import ENV

from utils import add_headers

app = Flask(__name__)
CORS(app)

app.config.from_object(ENV)


db = SQLAlchemy(app)


class VideoEntry(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    duration = db.Column(db.Integer)
    host = db.Column(db.String(250))
    ref_id = db.Column(db.String(50))
    hits = db.Column(db.Integer)
    src = db.Column(db.String(250))
    pic_src = db.Column(db.String(250))
    created = db.Column(db.Integer)
    last_checked = db.Column(db.Integer)

    def get_json(self):
        return {"title": self.title,
                "duration": "0" if self.duration is None else str(self.duration),
                "host": "" if self.host is None else str(self.host),
                "ref_id": "" if self.ref_id is None else str(self.ref_id),
                "hits": "0" if self.hits is None else str(self.hits),
                "src": "" if self.src is None else str(self.src),
                "pic_src": "" if self.pic_src is None else str(self.pic_src),
                "created": 0 if self.created is None else self.created,
                "last_checked": 0 if self.last_checked is None else self.last_checked
                }

    def __repr__(self):
        data = self.get_json()
        return repr(data)


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
    key = request.args.get('key') if request.args.get('key') is not None else ""
    page_no = int(request.args.get('page')) if request.args.get('page') is not None else 1
    descend = desc if request.args.get('desc') is not None else lambda *a, **k: None

    matches = db.session.query(VideoEntry) \
        .filter(VideoEntry.title.like("%" + key + "%")) \
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
