# -*- coding: utf-8 -*-

import logging

import time
import formencode
from formencode import htmlfill
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import restrict
from sqlalchemy.orm.exc import NoResultFound
from webhelpers.markdown import markdown

from horosh.lib.base import BaseController, render
from horosh.lib.utils import rest2html
from horosh.lib import helpers as h
from horosh.model import meta
from horosh import model

log = logging.getLogger(__name__)

class ArticleForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    article_title = formencode.validators.String(
        not_empty=True,
        messages={}
    )
    article_content = formencode.validators.String(
        not_empty=True,
        messages={}
    )
    
class ArticleController(BaseController):
    def _getArticle(self, id):
        try:
            node = meta.Session.query(model.Article).filter_by(id=int(id)).one()
        except NoResultFound:
            abort(404)
        return node
    
    def _redirectToDefault(self, id):
        url = h.url_for(controller='article', action='show', id=id)
        log.info(dir(url))
        if (request.is_xhr):
            c.url = url
            result = render('/util/redirect.html')
        else :
            response.status_int = 302
            response.headers['location'] = url
            result = "Moved temporarily"  
        return result
            
    def edit(self, id):
        node = self._getArticle(id)
        
        values = {
            'article_title': node.title,
            'article_content': node.content
        }
        c.title = node.title
        c.content = node.content
        if (request.is_xhr):
            result = htmlfill.render(render('/article/edit-form.html'), values)
        else :
            result = htmlfill.render(render('/article/edit.html'), values)
        return result
    
    @restrict('POST')
    @validate(schema=ArticleForm(), form='edit')
    def save(self, id):
        time.sleep(10)
        #log.info(request.POST['article_save'])
        node = self._getArticle(id)
        node.title = self.form_result['article_title']
        node.content = self.form_result['article_content']
        meta.Session.commit()
        return self._redirectToDefault(node.id)
    
    def new(self):
        return render('/article/new.html')

    @restrict('POST')
    @validate(schema=ArticleForm(), form='new')
    def create(self):
        data = {}
        data['title'] = self.form_result['article_title']
        data['content'] = self.form_result['article_content']
        data['filter'] = 'reStrucuredText'
        data['node_user_id'] = 1
        node = model.Article(**data)
        meta.Session.add(node)
        meta.Session.commit()
        return self._redirectToDefault(node.id)
    
    def show(self, id):
        node = self._getArticle(id)
            
        c.title = node.title
        c.content = rest2html(node.content)
        
        return render('/article/show.html')