from  sqlalchemy import create_engine
from  sqlalchemy.orm import sessionmaker
from hw2.model import (
    Base,
    BlogPost,
    Tag,
    Writer
)

class BlogDb:
    def __init__(self, url, base=Base):
        engine =create_engine(url)
        base.metadata.create_all(engine)
        session_db = sessionmaker(bind=engine)
        self.__session = session_db()

    @property
    def session(self):
        return self.__session

    def add_post(self, title:str, date:str, url:str, writer:Writer, tags=[]):
        tags_new = []
        if self.session.query(Writer).filter_by(url = writer.url).all():
            writer = self.session.query(Writer).filter_by(url = writer.url).first()
        else:
            self.session.add(writer)
        for tag in tags:
            if self.session.query(Tag).filter_by(name=tag).all():
                tags_new.append(self.session.query(Tag).filter_by(name=tag).first())
            else:
                tag_new = Tag(name = tag)
                tags_new.append(tag_new)
                self.session.add(tag_new)
        self.session.add(BlogPost(title = title, url = url, date= date, writer = writer, tags = tags_new))
        self.session.commit()

