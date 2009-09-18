# -*- coding: utf-8 -*-

import logging

import formencode
from formencode import htmlfill

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import restrict

from horosh.lib.base import BaseController, render

log = logging.getLogger(__name__)

class ContentForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    title = formencode.validators.String(
        not_empty=True,
        messages={}
    )
    content = formencode.validators.String(
        not_empty=True,
        messages={}
    )
    
class ArticleController(BaseController):

    def edit(self, id):
        return render('/article/edit.html')
    
    def new(self):
        return render('/article/new.html')

    @restrict('POST')
    @validate(schema=ContentForm(), form='new')
    def create(self):
        # Add the new content to the database
        content = model.Content()
        for k, v in self.form_result.items():
            setattr(content, k, v)
        meta.Session.add(content)
        meta.Session.commit()
        # Issue an HTTP redirect
        response.status_int = 302
        response.headers['location'] = h.url_for(controller='content',
            action='view', id=content.id)
        return "Moved temporarily"