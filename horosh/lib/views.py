# -*- coding: utf-8 -*-
from horosh.lib.base import current_user, render
from horosh.model import meta
from horosh import model
from sqlalchemy import and_
import logging

log = logging.getLogger(__name__)

def sidebar():
    articles = meta.Session.query(model.Article).filter(
        and_(model.Article.published != None, model.Article.label == None)
    ).order_by(model.Article.created.desc()).all()

    params = dict(
        user=current_user(),
        articles=articles
    )
    return render('/sidebar.html', params)
