# -*- coding: utf-8 -*-

"""Setup the horosh application"""
import logging

from horosh.config.environment import load_environment
from horosh.model import meta
from horosh import model

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup horosh here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)
    
    log.info("Adding root user")
    user = model.User(u"naspeh@pusto.org", "1")
    meta.Session.add(user)
    meta.Session.commit()
    
    log.info("Successfully set up.")