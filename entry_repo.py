from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import time

from entry import Base, VideoEntry
from settings import DB_NAME

engine = create_engine('sqlite:///' + DB_NAME + '.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


def insert_one(vid):
    now = time.time()
    vid.created = now
    vid.last_checked = now
    session.add(vid)
    session.commit()


def insert_many(vid_list):
    for vid in vid_list:
        now = time.time()
        vid.created = now
        vid.last_checked = now
        session.add(vid)
    session.commit()


def get_by_title(title):
    return session.query(VideoEntry).filter(VideoEntry.title.like("%"+title +"%")).all()


def get_range(from_id, to_id):
    return session.query(VideoEntry).filter(from_id <= VideoEntry.id).filter(VideoEntry.id <= to_id)
