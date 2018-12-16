from flask import Flask, request
from flask_cors import CORS

#import entry_repo as db
from entry import VideoEntry
from settings import PORT, HOST
from utils import add_headers

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import time

from entry import Base, VideoEntry
from settings import DB_NAME

engine = create_engine('sqlite:///' + DB_NAME + '.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


app = Flask(__name__)
CORS(app)


def insert_one(vid):
    now = time.time()
    vid.created = now
    vid.last_checked = now
    session.add(vid)
    session.commit()


# key = '', page_no=1, desc=true
@app.route("/videos", methods=['GET'])
def get_by_title():
    if 'key' in request.args:
        key = request.args.get('key')
        matches = session.query(VideoEntry).filter(VideoEntry.title.like("%" + key + "%")).all()
    elif 'from_id' in request.args and 'to_id' in request.args:
        from_id = request.args.get('from_id')
        to_id = request.args.get('to_id')
        session.query(VideoEntry).filter(from_id <= VideoEntry.id).filter(VideoEntry.id <= to_id)
    else:
        return add_headers({'result': 'Error in url args'}, 400)
    matches = [x.get_json() for x in matches]
    return add_headers(matches, 200)


@app.route("/videos", methods=['POST'])
def add_vid():
    insert_one(VideoEntry(**request.json))
    return add_headers({'result': 'OK'}, 200)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
