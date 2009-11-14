# -*- coding: utf-8 -*-

"""Setup the horosh application"""
from datetime import datetime
from horosh.config.environment import load_environment
from horosh.model import *
import logging

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup horosh here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)
    
    log.info('Adding root user')
    user = User('naspeh', 'naspeh@pusto.org', u'1')
    meta.Session.add(user)

    log.info('Adding first event')
    event = Event()
    event.title = u'Крым. Тарханкут. Барракуда'
    event.start = datetime.now()
    event.finish = datetime.now()
    event.node_user = user 
    meta.Session.add(event)

    log.info('Adding nobody user')
    user = User('nobody', 'nobody@pusto.org')
    meta.Session.add(user)
    
    meta.Session.commit()
    
    log.info("Successfully set up.")