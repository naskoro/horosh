# -*- coding: utf-8 -*-
from horosh.lib.base import render, current_user
from horosh.model import meta
from horosh import model
from sqlalchemy import and_
import logging

log = logging.getLogger(__name__)

def sidebar():
    articles = meta.Session.query(model.Article).filter(
        and_(model.Article.published != None, model.Article.label == None)
    ).order_by(model.Article.created.desc()).all()

    pulse = meta.Session.query(model.Article).filter(
        and_(model.Article.published != None, model.Article.label == 'pulse')
    ).order_by(model.Article.created.desc()).all()

    params = dict(
        articles=articles,
        pulse=pulse
    )
    return render('/sidebar.html', params)
