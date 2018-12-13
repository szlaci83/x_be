from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time

from entry import Base, VideoEntry
from settings import DB_NAME
from flask_sqlalchemy import SQLAlchemy

engine = create_engine('sqlite:///' + DB_NAME + '.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


def insert(vid):
    session.add(vid)
    session.commit()


def query():
    vid = session.query(VideoEntry).filter(VideoEntry.title.like("%sam%")).first()
    #vid = session.query(VideoEntry).first()
    return vid


if __name__ == '__main__':
    new_vid = VideoEntry(title="sample24", created=int(time.time()))
    insert(new_vid)
    print(str(query()))
