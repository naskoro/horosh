# -*- coding: utf-8 -*-

from hashlib import md5
from horosh.lib.util import rst2html
from horosh.model import db, meta
from sqlalchemy import orm
import logging


log = logging.getLogger(__name__)

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""

    sessionmaker = orm.sessionmaker(autoflush=True, autocommit=False, bind=engine)

    meta.engine = engine
    meta.Session = orm.scoped_session(sessionmaker)
    
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
    def __repr__(self):
        return "<Path('%s', '%s')>" % (self.path, self.node_id)

class Album(Node):
    def __init__(self):
        self.type = 'picasa'
        
    def __repr__(self):
        return "<Album('%s', '%s', '%s')>" % (self.id, self.settings, self.type)

class Article(Node):
    @property
    def html_content(self):
        return rst2html(self.content)
    
    def __repr__(self):
        return "<Article('%s')>" % self.id

class Report(Node):
    @property
    def number(self):
        return self.event.reports.index(self) + 1
    @property
    def html_content(self):
        return rst2html(self.content)
    
    def __repr__(self):
        return "<Report('%s')>" % self.id

class Event(Node):
    def report_by_number(self, number):
        try:
            node = self.reports[int(number)-1]
            return node
        except IndexError:
            return None
    @property
    def date(self):
        date, format = '', ''
        f_day, f_month, f_year = '%d ', '%b ', '%Y'
        
        if self.start.year == self.finish.year:
            date = self.start.strftime(f_year)
        else:
            format = f_year
            
        if self.start.month == self.finish.month:
            date = self.start.strftime(f_month) + date
        else:
            format = f_month + format
            
        if self.start.day == self.finish.day:
            date = self.start.strftime(f_day) + date
        else:
            format = f_day + format
            
        if format:
            date = self.start.strftime(format) + ' - '  + self.finish.strftime(format) + ' '  + date
            
        return date
     
    def __repr__(self):
        return "<Event('%s', '%s', '%s', '%s')>" % (self.id, self.title, self.start, self.finish)

class Person(Node):
    def __repr__(self):
        return "<Person('%s', '%s', '%s')>" % (self.id, self.nickname, self.email)

orm.mapper(Path, db.path, 
    properties={
        'node': orm.relation(Node),
    }
)
orm.mapper(Node, db.node, 
    properties={
        'node_user_id': db.node.c.user_id,
        'node_type': db.node.c.type,
        'node_user': orm.relation(User),
        'node_paths': orm.relation(Path),
    },
    polymorphic_on=db.node.c.type, polymorphic_identity='node'
)
orm.mapper(Album, db.album,
    properties={
        'events': orm.relation(Event, secondary=db.event_album),
    },
    inherits=Node, polymorphic_identity='album'
)
orm.mapper(Report, db.report, 
    properties={
        'event': orm.relation(
            Event,
            primaryjoin=db.report.c.event_id==db.event.c.id,
        ),
    },
    inherits=Node, polymorphic_identity='report'
)
orm.mapper(Article, db.article, 
    properties={
    },
    inherits=Node, polymorphic_identity='article'
)
orm.mapper(Event, db.event, 
    properties={
        'albums': orm.relation(Album, secondary=db.event_album),
        'reports': orm.relation(
            Report,
            primaryjoin=db.report.c.event_id==db.event.c.id,
        ),
        'persons': orm.relation(Person, secondary=db.event_person),
    },
    inherits=Node, polymorphic_identity='event'
)
orm.mapper(Person, db.person,
    properties={
        'user': orm.relation(User),
        'events': orm.relation(Event, secondary=db.event_person),
    },
    inherits=Node, polymorphic_identity='person'
)
orm.mapper(User, db.user,
    properties={
        'persons': orm.relation(
            Person, 
            primaryjoin=db.person.c.user_id==db.user.c.id, 
            cascade='all'
        )
    }
)