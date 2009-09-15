# -*- coding: utf-8 -*-

"""The application's tables definition"""
from sqlalchemy import schema, types
from datetime import datetime

from horosh.model import meta

user = schema.Table('user', meta.metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('user_id__seq', optional=True), primary_key=True),

    schema.Column('email', types.Unicode(50), nullable=False, unique=True),
    schema.Column('password', types.String(32)),    

    schema.Column('active', types.Unicode(32)),
    schema.Column('created', types.DateTime(), default=datetime.now()),
)

node = schema.Table('node', meta.metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('node_id__seq', optional=True), primary_key=True),
    schema.Column('user_id', types.Integer,
        schema.ForeignKey('user.id'), nullable=False),
    schema.Column('type', types.String(20), nullable=False),
)

person = schema.Table('person', meta.metadata,
    schema.Column('id', types.Integer,
        schema.ForeignKey('node.id'), primary_key=True),
    schema.Column('user_id', types.Integer,
        schema.ForeignKey('user.id'), nullable=True),

    schema.Column('email', types.Unicode(50), nullable=False),
    schema.Column('nickname', types.Unicode(20)),    
    schema.Column('fullname', types.Unicode(50)),

    schema.Column('created', types.DateTime(), default=datetime.now()),
    schema.Column('updated', types.DateTime(), onupdate=datetime.now())
)

path = schema.Table('path', meta.metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('path_id__seq', optional=True), primary_key=True),
    schema.Column('node_id', types.Integer,
        schema.ForeignKey('node.id'), nullable=False),

    schema.Column('path', types.Unicode(250), unique=True),
)

article = schema.Table('article', meta.metadata,
    schema.Column('id', types.Integer,
        schema.ForeignKey('node.id'), primary_key=True),
    
    schema.Column('body', types.Unicode(), nullable=False),
    schema.Column('filter', types.Unicode(10)),
    
    schema.Column('created', types.DateTime(), default=datetime.now()),
    schema.Column('updated', types.DateTime(), onupdate=datetime.now())
)

album = schema.Table('album', meta.metadata,
    schema.Column('id', types.Integer,
        schema.ForeignKey('node.id'), primary_key=True),
    
    schema.Column('path', types.Unicode(250), nullable=False),
    schema.Column('type', types.String(20)),
    
    schema.Column('created', types.DateTime(), default=datetime.now()),
)

event = schema.Table('event', meta.metadata,
    schema.Column('id', types.Integer,
        schema.ForeignKey('node.id'), primary_key=True),

    schema.Column('title', types.Unicode(250), nullable=False),
    schema.Column('notice', types.Unicode(1000)),
    schema.Column('start', types.Date(), nullable=False),
    schema.Column('finish', types.Date(), nullable=False),
    schema.Column('publish', types.Boolean, default=False),

    schema.Column('created', types.DateTime(), default=datetime.now()),
    schema.Column('updated', types.DateTime(), onupdate=datetime.now())
)

event_person = schema.Table('event_person', meta.metadata,
    schema.Column('event_id', types.Integer,
        schema.ForeignKey('event.id'), nullable=False),
    schema.Column('person_id', types.Integer,
        schema.ForeignKey('person.id'), nullable=False),
)

event_album = schema.Table('event_album', meta.metadata,
    schema.Column('event_id', types.Integer,
        schema.ForeignKey('event.id'), nullable=False),
    schema.Column('album_id', types.Integer,
        schema.ForeignKey('album.id'), nullable=False),
)

event_article = schema.Table('event_article', meta.metadata,
    schema.Column('event_id', types.Integer,
        schema.ForeignKey('event.id'), nullable=False),
    schema.Column('article_id', types.Integer,
        schema.ForeignKey('article.id'), nullable=False),
)

article_album = schema.Table('article_album', meta.metadata,
    schema.Column('article_id', types.Integer,
        schema.ForeignKey('article.id'), nullable=False),
    schema.Column('album_id', types.Integer,
        schema.ForeignKey('album.id'), nullable=False),
)