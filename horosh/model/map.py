# -*- coding: utf-8 -*-

from hashlib import md5
from horosh.lib.util import rst2html
from horosh.model import db, meta
from pytils import translit
from pytils.dt import ru_strftime
from routes import url_for
from sqlalchemy import orm
import gdata
import logging
import time

__all__ = ('init_model', 'Base', 'User', 'Node', 'Album', 'Article', 
    'Report', 'Event', 'Person')

log = logging.getLogger(__name__)

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""

    sessionmaker = orm.sessionmaker(autoflush=True, autocommit=False, bind=engine)

    meta.engine = engine
    meta.Session = orm.scoped_session(sessionmaker)

class Base(object):
    def __unicode__(self):
        raise NotImplemented
    def __repr__(self):
        return self.__unicode__().encode('utf-8')
    
class User(Base):
    def url(self):
        return url_for(controller='event', action='list', user=self.nickname)
    
    def __init__(self, nickname, email, password=None):
        self.email = email
        self.nickname = nickname
        if (password):
            self.password = md5(password).hexdigest()
            
    def __unicode__(self):
        return "<User('%s', '%s')>" % (self.nickname, self.email)

class Node(Base):
    def __init__(self, node_user_id=None):
        self.node_user_id = node_user_id
        
    def __unicode__(self):
        return "<Node('%s')>" % self.id

class Album(Node):
    def __init__(self):
        self.type = 'picasa'

    def url_edit(self, **kwargs):
        return url_for(
            controller='album', action='edit', 
            id=self.id, **kwargs
        )

    def url_remove(self, **kwargs):
        return url_for(
            controller='album', action='remove', 
            id=self.id, **kwargs
        )

    def url_to_picasa(self):
        photos = gdata.GDataFeedFromString(self.settings)
        return photos.GetAlternateLink().href
        
    def __unicode__(self):
        return "<Album('%s', '%s', '%s')>" % (self.id, self.settings, self.type)

class Article(Node):
    @property
    def html_content(self):
        return rst2html(self.content)

    def url(self):
        return url_for(controller='article', action='show', path=self.path)

    def url_edit(self):
        return url_for(controller='article', action='edit', id=self.id)

    def url_remove(self):
        return url_for(controller='article', action='remove', id=self.id)

    def url_publish(self, published=True):
        if published:
            published = 1
        else:
            published = 0
            
        return url_for(
            controller='article', action='publish', 
            id=self.id, published=published
        )
    
    def __unicode__(self):
        return "<Article('%s')>" % self.id

class Report(Node):
    def url(self):
        return url_for(
            controller='report', action='show', title=self.event.slug,
            event_id=self.event_id, id=self.number
        )

    def url_edit(self):
        return url_for(
            controller='report', action='edit', 
            event_id=self.event_id, id=self.number
        )

    def url_remove(self):
        return url_for(
            controller='report', action='remove', 
            event_id=self.event_id, id=self.number
        )
    
    def full_title(self):
        titles = [u'Отчет №%s' % self.number]
        if self.title:
            titles.append(self.title)
        return '. '.join(titles)
    @property
    def number(self):
        return self.event.reports.index(self) + 1
    
    @property
    def html_content(self):
        return rst2html(self.content)
    
    def __unicode__(self):
        return "<Report('%s')>" % self.id

class Event(Node):
    @property
    def slug(self):
        return translit.slugify(self.title)
    
    def url(self):
        return url_for(
            controller='event', action='show', 
            title=self.slug, id=self.id
        )

    def url_edit(self):
        return url_for(controller='event', action='edit', id=self.id)

    def url_remove(self):
        return url_for(controller='event', action='remove', id=self.id)

    def url_publish(self, published=True):
        if published:
            published = 1
        else:
            published = 0
            
        return url_for(
            controller='event', action='publish', 
            id=self.id, published=published
        )

    def url_add_report(self):
        return url_for(controller='report', action='new', event_id=self.id)

    def url_add_person(self):
        return url_for(controller='person', action='new', event_id=self.id)

    def url_add_album(self):
        return url_for(controller='album', action='new', event_id=self.id)
        
    def report_by_number(self, number):
        try:
            node = self.reports[int(number)-1]
            return node
        except IndexError:
            return None
        
    def persons_fullnames(self):
        persons = []
        for person in self.persons:
            persons.append(person.fullname)
        return persons
            
    @property
    def date(self):
        date, format = '', ''
        f_day, f_month, f_year = u'%d ', u'%B ', u'%Y'
        
        if self.start.year == self.finish.year:
            date = ru_strftime(f_year, date=self.start)
        else:
            format = f_year
            
        if self.start.month == self.finish.month:
            date = ru_strftime(f_month, date=self.start, inflected=True) + date
        else:
            format = f_month + format
            
        if self.start.day == self.finish.day:
            date = ru_strftime(f_day, date=self.start) + date
        else:
            format = f_day + format
            
        if format:
            date = '%s - %s %s' % (
                ru_strftime(format, date=self.start, inflected=True), 
                ru_strftime(format, date=self.finish, inflected=True), 
                date
            )
            
        return date
     
    def __unicode__(self):
        return "<Event('%s', '%s', '%s')>" % (self.id, self.title, self.published)

class Person(Node):
    def url(self):
        return url_for(
            controller='person', action='show', 
            event_id=self.event_id, id=self.id
        )

    def url_edit(self):
        return url_for(
            controller='person', action='edit', 
            event_id=self.event_id, id=self.id
        )

    def url_remove(self):
        return url_for(
            controller='person', action='remove', 
            event_id=self.event_id, id=self.id
        )

    def url_avatar(self, with_time=False):
        params = dict(controller='person', action='avatar', id=self.id)
        if with_time:
            params['time'] = time.time()
        return url_for(**params)
    
    def __unicode__(self):
        return "<Person('%s', '%s')>" % (self.id, self.fullname)

orm.mapper(Node, db.node, 
    properties={
        'node_user_id': db.node.c.user_id,
        'node_type': db.node.c.type,
        'node_user': orm.relation(User)
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
        'persons': orm.relation(
            Person, 
            primaryjoin=db.person.c.event_id==db.event.c.id,
        ),
    },
    inherits=Node, polymorphic_identity='event'
)
orm.mapper(Person, db.person,
    properties={
        'user': orm.relation(User),
        'event': orm.relation(
            Event,
            primaryjoin=db.person.c.event_id==db.event.c.id,
        ),
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