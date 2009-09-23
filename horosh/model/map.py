# -*- coding: utf-8 -*-

from sqlalchemy import orm
from hashlib import md5
import logging

from horosh.model import meta
from horosh.model import db

log = logging.getLogger(__name__)

class User(object):
    def __init__(self, email, password=None):
        self.email = email
        if (password):
            self.password = md5(password).hexdigest()
    def __repr__(self):
        return "<User('%s')>" % self.email

class Node(object):
    def __init__(self, node_user_id=None):
        self.node_user_id = node_user_id
    def __repr__(self):
        return "<Node('%s')>" % self.id

class Path(object):
    def __init__(self, path, node_id):
        self.path = path
        self.node_id = node_id
    def __repr__(self):
        return "<Path('%s', '%s')>" % (self.path, self.node_id)

class Album(Node):
    def __init__(self, username, albumid, node_user_id):
        self.settings = {'username': username, 'albumid': albumid}
        self.type = 'picasa'
        Node.__init__(self, node_user_id)
        
    def __repr__(self):
        return "<Album('%s', '%s', '%s')>" % (self.id, self.settings, self.type)

    @property
    def settingsUser(self):
        return self.settings['username']
    @property
    def settingsId(self):
        return self.settings['albumid']

class AlbumPicasa(Album):
    album = None

class Article(Node):
    def __init__(self, title, content, filter, node_user_id=None):
        self.title = title
        self.content = content
        self.filter = filter
        Node.__init__(self, node_user_id)
    def __repr__(self):
        return "<Article('%s')>" % self.id

class Event(Node):
    def __init__(self, user_id, title, notice, start, finish, publish=False, node_user_id=None):
        self.title = title
        self.notice = notice
        self.start = start
        self.finish = finish
        self.publish = publish
        Node.__init__(self, node_user_id)
    def __repr__(self):
        return "<Event('%s')>" % self.id

class Person(Node):
    def __init__(self, email, nickname, fullname, user_id=None, node_user_id=None):
        self.email = email
        self.nickname = nickname
        self.fullname = fullname
        self.user_id = user_id
        Node.__init__(self, node_user_id)
    def __repr__(self):
        return "<Person('%s', '%s', '%s')>" % (self.id, self.nickname, self.email)

def mapped ():
    orm.mapper(Path, db.path, 
        properties={
            'node': orm.relation(Node),
        }
    )
    orm.mapper(Node, db.node, 
        properties={
            'node_user_id': db.node.c.user_id,
            'node_type': db.node.c.type,
            'node_owner': orm.relation(User),
            'node_paths': orm.relation(Path),
        },
        polymorphic_on=db.node.c.type, polymorphic_identity='node'
    )
    orm.mapper(Album, db.album,
        properties={
        },
        inherits=Node, polymorphic_identity='album'
    )
    orm.mapper(Article, db.article, 
        properties={
            'albums': orm.relation(Album, secondary=db.article_album),
        },
        inherits=Node, polymorphic_identity='article'
    )
    orm.mapper(Event, db.event, 
        properties={
            'albums': orm.relation(Album, secondary=db.event_album),
            'reports': orm.relation(Article, secondary=db.event_article),
            'members': orm.relation(Person, secondary=db.event_person),
        },
        inherits=Node, polymorphic_identity='event'
    )
    orm.mapper(Person, db.person,
        properties={
            'user': orm.relation(User),
        },
        inherits=Node, polymorphic_identity='person'
    )
    orm.mapper(User, db.user,
        properties={
            'persons': orm.relation(Person, primaryjoin=db.person.c.user_id==db.user.c.id)
        }
    )

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""

    sessionmaker = orm.sessionmaker(autoflush=True, autocommit=False, bind=engine)

    meta.engine = engine
    meta.Session = orm.scoped_session(sessionmaker)