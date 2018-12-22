from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

