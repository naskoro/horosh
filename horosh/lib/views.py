# -*- coding: utf-8 -*-
from horosh.lib.base import render, current_user
from horosh.model import meta
from horosh import model, form
from pylons import request, tmpl_context as c, session
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

class LoginForm(form.FieldSet):
    def init(self):
        self.adds(
            form.Field('username', validator=form.v.String(not_empty=True, min=3, max=30)),
            form.Field('password', validator=form.v.String(not_empty=True)),
            form.Field('send'),
        )

def login():
    fs = LoginForm('')

    if request.POST and fs.is_valid(request.POST):
        return

    c.form = fs
    c.fs = fs.fields

    result = render('/util/login.html')
    if request.POST:
        result = fs.htmlfill(result)
    result = result.replace('%', '%%')
    return result
