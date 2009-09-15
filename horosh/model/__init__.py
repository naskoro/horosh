# -*- coding: utf-8 -*-

"""The application's model objects"""
from sqlalchemy import orm

from horosh.model import meta
from horosh.model import db
from hashlib import md5

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""

    sessionmaker = orm.sessionmaker(autoflush=True, autocommit=False, bind=engine)

    meta.engine = engine
    meta.Session = orm.scoped_session(sessionmaker)

class Node(object):
    pass

class NodeInstance(object):
    def __init__(self):
        node = Node()
        meta.Session.add(node)
        meta.Session.flush()
        self.node_id = node.id

class Album(NodeInstance):
    def __init__(self, path, type):
        self.path = path
        self.type = type
        super.__init__() 

class Article(NodeInstance):
    def __init__(self, body, filter):
        self.body = body
        self.filter = filter
        super.__init__()

class Event(NodeInstance):
    def __init__(self, title, notice, start, finish, publish=False):
        self.title = title
        self.notice = notice
        self.start = start
        self.finish = finish
        self.publish = publish
        super.__init__()

class Path(object):
    pass

class Person(NodeInstance):
    pass

class User(object):
    def __init__(self, email, password):
        self.email = email
        self.password = md5(password).hexdigest()
    def __repr__(self):
        return self.__class__.__name__ + " " + self.email
    
orm.mapper(Album, db.album, properties={
    'node': orm.relation(Node, backref="album"),
})
orm.mapper(Article, db.article, properties={
    'node': orm.relation(Node, backref="article"),                                             
    'albums': orm.relation(Album, secondary=db.article_album),
})
orm.mapper(Event, db.event, properties={
    'node': orm.relation(Node, backref="event"),
    'albums': orm.relation(Album, secondary=db.event_album),
    'reports': orm.relation(Article, secondary=db.event_article),
    'members': orm.relation(Person, secondary=db.event_person),
})
orm.mapper(Node, db.node, properties={
    'owner': orm.relation(User),
})
orm.mapper(Path, db.path)
orm.mapper(Person, db.person)
orm.mapper(User, db.user, properties={
    'persons': orm.relation(Person, backref="user")
})