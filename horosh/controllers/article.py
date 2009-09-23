# -*- coding: utf-8 -*-

import logging
import time

import formencode as form
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import restrict
from sqlalchemy.orm.exc import NoResultFound

from horosh.lib.base import BaseController, render
from horosh.lib.util import rest2html, getCurrentUser
from horosh.model import meta
from horosh import model

log = logging.getLogger(__name__)

class ArticleForm(form.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    article_title = form.validators.String(
        not_empty=True,
        messages={}
    )
    article_album_user =  form.validators.String()
    article_album_id =  form.validators.String()
    article_content = form.validators.String(
        not_empty=True,
        messages={}
    )
    
class ArticleController(BaseController):
    def new(self):
        return render('/article/new.html')

    @restrict('POST')
    @validate(schema=ArticleForm(), form='new')
    def create(self):
        data = {}
        data['title'] = self.form_result['article_title']
        data['content'] = self.form_result['article_content']
        data['filter'] = 'reStrucuredText'
        data['node_user_id'] = getCurrentUser().id
        node = model.Article(**data)
        meta.Session.add(node)
        meta.Session.commit()
        return self._redirectToDefault(node.id)
    
    def show(self, id):
        node = self._getArticle(id)
            
        c.title = node.title
        c.content = rest2html(node.content)
        
        return render('/article/show.html')            
    def edit(self, id):
        node = self._getArticle(id)
        
        values = {
            'article_title': node.title,
            'article_content': node.content
        }
        
        if (node.albums):
            album = node.albums[0]
            values.update({
                'article_album_user': album.settingsUser,
                'article_album_id': album.settingsId
            })
        c.title = node.title
        if (request.is_xhr):
            result = form.htmlfill.render(render('/article/edit_form.html'), values)
        else :
            result = form.htmlfill.render(render('/article/edit.html'), values)
        return result
    
    @restrict('POST')
    @validate(schema=ArticleForm(), form='edit')
    def save(self, id):
        #time.sleep(5)
        #log.info(request.POST['article_save'])
        node = self._getArticle(id)
        node.title = self.form_result['article_title']
        node.content = self.form_result['article_content']
        
        album_user = self.form_result['article_album_user']
        album_id = self.form_result['article_album_id'] 
        if (album_user and album_id):
            node.albums = [model.Album(
                album_user,
                album_id,
                getCurrentUser().id
            )]
        
        meta.Session.commit()
        return self._redirectToDefault(node.id)

    def _getArticle(self, id):
        try:
            node = meta.Session.query(model.Article).filter_by(id=int(id)).one()
        except NoResultFound:
            abort(404)
        return node
    
    def _redirectToDefault(self, id):
        url = {'controller': 'article', 'action': 'show', 'id': id}
        log.info(dir(url))
        if (request.is_xhr):
            c.url = url
            result = render('/util/redirect.html')
        else :
            redirect_to(**url)
            result = "Moved temporarily"  
        return result
