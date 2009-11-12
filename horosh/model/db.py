# -*- coding: utf-8 -*-

"""The application's tables definition"""
from datetime import datetime
from horosh.model import meta
from sqlalchemy import schema, types


user = schema.Table('user', meta.metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('user_id__seq', optional=True), primary_key=True),

    schema.Column('nickname', types.String(20), nullable=False, unique=True),
    schema.Column('email', types.String(50), nullable=False, unique=True),
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
    schema.Column('event_id', types.Integer, 
        schema.ForeignKey('event.id'), nullable=False),

    schema.Column('fullname', types.Unicode(50), nullable=False),
    schema.Column('avatar', types.Binary()),
    schema.Column('details', types.Unicode(500)),

    schema.Column('created', types.DateTime(), default=datetime.now()),
    schema.Column('updated', types.DateTime(), onupdate=datetime.now())
)

path = schema.Table('path', meta.metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('path_id__seq', optional=True), primary_key=True),
    schema.Column('node_id', types.Integer,
        schema.ForeignKey('node.id'), nullable=False),

    schema.Column('path', types.Unicode(250), unique=True),
    schema.Column('used', types.Boolean),
    
    schema.Column('updated', types.DateTime(), onupdate=datetime.now())
)

article = schema.Table('article', meta.metadata,
    schema.Column('id', types.Integer,
        schema.ForeignKey('node.id'), primary_key=True),
    
    schema.Column('title', types.Unicode()),
    schema.Column('content', types.Unicode(), nullable=False),
    schema.Column('filter', types.Unicode(20), nullable=False),
    schema.Column('published', types.DateTime),
    
    schema.Column('created', types.DateTime(), default=datetime.now()),
    schema.Column('updated', types.DateTime(), onupdate=datetime.now())
)

album = schema.Table('album', meta.metadata,
    schema.Column('id', types.Integer,
        schema.ForeignKey('node.id'), primary_key=True),
    
    schema.Column('settings', types.PickleType(), nullable=False),
    schema.Column('type', types.String(20)),
    
    schema.Column('created', types.DateTime(), default=datetime.now()),
)

event = schema.Table('event', meta.metadata,
    schema.Column('id', types.Integer,
        schema.ForeignKey('node.id'), primary_key=True),
    schema.Column('title', types.Unicode(250), nullable=False),
    schema.Column('summary', types.Unicode(1000)),
    schema.Column('start', types.Date(), nullable=False),
    schema.Column('finish', types.Date(), nullable=False),
    schema.Column('published', types.DateTime),

    schema.Column('created', types.DateTime(), default=datetime.now()),
    schema.Column('updated', types.DateTime(), onupdate=datetime.now())
)

report = schema.Table('report', meta.metadata,
    schema.Column('id', types.Integer,
        schema.ForeignKey('node.id'), primary_key=True),
    schema.Column('event_id', types.Integer, 
        schema.ForeignKey('event.id'), nullable=False),
        
    schema.Column('title', types.Unicode()),
    schema.Column('content', types.Unicode(), nullable=False),
    schema.Column('filter', types.Unicode(20), nullable=False),
    schema.Column('published', types.DateTime),
    
    schema.Column('created', types.DateTime(), default=datetime.now()),
    schema.Column('updated', types.DateTime(), onupdate=datetime.now())
)

event_album = schema.Table('event_album', meta.metadata,
    schema.Column('event_id', types.Integer,
        schema.ForeignKey('event.id'), nullable=False),
    schema.Column('album_id', types.Integer,
        schema.ForeignKey('album.id'), nullable=False),
)