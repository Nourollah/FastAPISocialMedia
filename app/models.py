from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import sqltypes, expression
from sqlalchemy.orm import relationship


class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer,
                primary_key=True,
                index=True)
    title = Column(String,
                   nullable=False)
    content = Column(String,
                     nullable=False)
    published = Column(Boolean,
                       server_default="TRUE",
                       nullable=False)
    created_at = Column(sqltypes.TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=expression.text("now()"))
    owner_id = Column(Integer,
                      ForeignKey('users.id',
                                 ondelete='CASCADE',
                                 onupdate='CASCADE'),
                      nullable=False)

    owner = relationship('Users')

    def __init__(self, title, content, owner_id, published=True):
        self.title = title
        self.content = content
        self.owner_id = owner_id
        self.published = published

    def __repr__(self):
        return f"<Posts {self.id} {self.title} {self.content} {self.owner_id} {self.published}>"

    def dict(self):
        return {"title": self.title, "content": self.content, "id": self.owner_id, "published": self.published}


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(sqltypes.TIMESTAMP(timezone=True), nullable=False, server_default=expression.text("now()"))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<Users {self.id} {self.name} {self.email} {self.password}>"

    def __str__(self):
        return f"<Users {self.id} {self.name} {self.email} {self.password}>"

    def dict(self):
        return {"name": self.name, "email": self.email, "password": self.password}
