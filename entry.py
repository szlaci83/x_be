from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class VideoEntry(Base):
    __tablename__ = 'video'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    duration = Column(Integer)
    host = Column(String(250))
    ref_id = Column(String(50))
    hits = Column(Integer)
    src = Column(String(250))
    pic_src = Column(String(250))
    created = Column(Integer)
    last_checked = Column(Integer)

    def get_json(self):
        return {"title": self.title,
                "duration": 0 if self.duration is None else self.duration,
                "host": "" if self.host is None else self.host,
                "ref_id": "" if self.ref_id is None else self.ref_id,
                "hits": 0 if self.hits is None else self.hits,
                "src": "" if self.src is None else self.src,
                "pic_src": "" if self.pic_src is None else self.pic_src,
                "created" : 0 if self.created is None else self.created,
                "last_checked": 0 if self.last_checked is None else self.last_checked
                }

    def __repr__(self):
        return self.get_json()


if __name__ == '__main__':
    engine = create_engine('sqlite:///videos_example.db')
    Base.metadata.create_all(engine)



