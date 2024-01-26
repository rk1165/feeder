from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Feed(db.Model):
    __tablename__ = 'feeds'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    path = db.Column(db.String, nullable=False)
    item_tag = db.Column(db.String, nullable=False)
    item_cls = db.Column(db.String, nullable=False)
    title_tag = db.Column(db.String, nullable=False)
    title_cls = db.Column(db.String, nullable=True)
    link_tag = db.Column(db.String, nullable=False)
    link_cls = db.Column(db.String, nullable=True)
    description_tag = db.Column(db.String, nullable=True)
    description_cls = db.Column(db.String, nullable=True)

    def __init__(self, title, url, description, path, item_tag, item_cls,
                 title_tag, title_cls, link_tag, link_cls, description_tag, description_cls):
        self.title = title
        self.url = url
        self.description = description
        self.path = path
        self.item_tag = item_tag
        self.item_cls = item_cls
        self.title_tag = title_tag
        self.title_cls = title_cls
        self.link_tag = link_tag
        self.link_cls = link_cls
        self.description_tag = description_tag
        self.description_cls = description_cls

    def __repr__(self):
        return (f"<Feed: {self.id=} {self.title=} {self.url=} {self.description=}"
                f"({self.item_tag=}, {self.item_cls=})\n"
                f"({self.title_tag=}, {self.title_cls=})\n"
                f"({self.link_tag=}, {self.link_cls=})\n"
                f"({self.description_tag=}, {self.description_cls})>")