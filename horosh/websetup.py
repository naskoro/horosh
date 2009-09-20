# -*- coding: utf-8 -*-

"""Setup the horosh application"""
import logging

from horosh.config.environment import load_environment
from horosh.model import meta
from horosh.model import * 

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup horosh here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)
    
    log.info("Adding root user")
    user = User("naspeh@pusto.org", u"1")
    meta.Session.add(user)
    
    meta.Session.commit()
    
    # Test models
    if(False):
        log.info("Adding album")
        album = Album({'username':'naspeh', 'albumid':"google.com"}, "picasa", user.id)
        meta.Session.add(album)
    
        log.info("Adding persons")
    
        person1 = Person("naspeh@pusto.org", u"naspeh", u"Na Speh", None, user.id)
        meta.Session.add(person1)
        log.info("person1: %s" % person1)
        
        person2 = Person("naspeh@pusto.org", u"naspeh", u"Na Speh", user.id, user.id)
        meta.Session.add(person2)
        log.info("person2: %s" % person2)
        
        meta.Session.commit()
        
        album = meta.Session.query(Album).all()[0]
        log.info("album.settings: %s" % album.settings)
        log.info("album.node_owner: %s" % album.node_owner)
        log.info("album.node_paths: %s" % album.node_paths)
        
    log.info("Successfully set up.")