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
from horosh.lib.util import rest2html, get_current_user
from horosh.model import meta
from horosh import model
from horosh import forms

log = logging.getLogger(__name__)

fs = forms.FieldSet('article',
    forms.Field('title', validator=forms.v.String(not_empty=True)),
    forms.Field('album_user', validator=forms.v.String()),
    forms.Field('album_id', validator=forms.v.String()),
    forms.Field('content', validator=forms.v.String(not_empty=True))
)
    
class ArticleController(BaseController):
    @validate(schema=fs.schema, form='new')
    def new(self):
        if request.POST:
            fs.set_values(self.form_result, use_ids=True)
            
            node = model.Article()
            node.title = fs.get_value('title')
            node.content = fs.get_value('content')
            node.filter = 'reStrucuredText'
            node.node_user_id = get_current_user().id
            
            meta.Session.add(node)
            meta.Session.commit()
            return self._redirect_to_default(node.id)
            
        return render('/article/new.html')

    def show(self, id):
        node = self._get_article(id)
            
        c.title = node.title
        c.content = rest2html(node.content)
        
        return render('/article/show.html')

    @fs.validate(form='edit')            
    def edit(self, id):
        node = self._get_article(id)
        if request.POST:
            fs.set_values(self.form_result, use_ids=True)
            
            node.title = fs.get_value('title')
            node.content = fs.get_value('content')
            
            album_user = fs.get_value('album_user')
            album_id = fs.get_value('album_id') 
            if (album_user and album_id):
                node.albums = [model.Album(
                    album_user,
                    album_id,
                    get_current_user().id
                )]
            
            meta.Session.commit()
            return self._redirect_to_default(node.id)

        fs.set_values({
            'title': node.title,
            'content': node.content
        })
        
        if (node.albums):
            album = node.albums[0]
            fs.set_values({
                'album_user': album.settingsUser,
                'album_id': album.settingsId
            })
        c.title = node.title
        
        if (request.is_xhr):
            result = fs.render('/article/edit_form.html')
        else :
            result = fs.render('/article/edit.html')
        return result
    
    def _get_article(self, id):
        try:
            node = meta.Session.query(model.Article).filter_by(id=int(id)).one()
        except NoResultFound:
            abort(404)
        return node
    
    def _redirect_to_default(self, id):
        return self._redirect_to(controller='article', action='show', id=id)