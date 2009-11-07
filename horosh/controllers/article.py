# -*- coding: utf-8 -*-

from horosh import form, model
from horosh.lib.base import BaseController, render, is_ajax
from horosh.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
import logging
import time

log = logging.getLogger(__name__)

DEFAULT_FILTER = 'reStrucuredText'

class ArticleForm(form.FieldSet):
    def init(self):
        self.adds(
            form.Field('title', validator=form.v.String()),
            form.Field('content', validator=form.v.String(not_empty=True)),
            form.Field('save'),
            form.Field('cancel')
        )
    
class ArticleController(BaseController):
    def new(self, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)
        
        fs = ArticleForm('article-new')

        if request.POST and fs.fields.cancel.id in request.POST:
            return self._redirect_to_default(event_node.id)
        
        if request.POST and fs.is_valid(request.POST):
            node = model.Article()
            node.title = fs.fields.title.value
            node.content = fs.fields.content.value
            node.filter = DEFAULT_FILTER 
            node.node_user_id = session['current_user'].id
            
            meta.Session.add(node)
            event_node.articles.append(node)
            meta.Session.commit()
            
            return self._redirect_to_default(event_node.id)
        
        c.form = fs
        c.fs = fs.fields
        
        if is_ajax():
            result = render('/article/new_partial.html')
        else:
            result = render('/article/new.html')
        if request.POST:
            result = fs.htmlfill(result)
        return result

    def show(self, id):
        c.node = self._get_row(model.Article, id) 
        return render('/article/show.html')

    def edit(self, id):
        fs = ArticleForm('article-edit')
        node = self._get_row(model.Article, id)
        if request.POST and fs.is_valid(request.POST):
            time.sleep(5)
            
            node.title = fs.fields.title.value
            node.content = fs.fields.content.value
            
            album_user = fs.fields.album_user.value
            album_id = fs.fields.album_id.value 
            if (album_user and album_id):
                node.albums = [model.Album(
                    album_user,
                    album_id,
                    session['current_user'].id
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
                'album_user': album.settings_user,
                'album_id': album.settings_id
            })
        c.fs = fs.fields
        c.title = node.title
        return fs.render('/article/edit.html', '/article/edit_form.html')

    def remove(self, id, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)
        node = self._get_row(model.Article, id)
        self._event_has_article(event_node, node)
        
        meta.Session.delete(node)
        meta.Session.commit()
        return self._redirect_to_default(event_node.id)
    
    def _event_has_article(self, event, article):
        for item in event.articles:
            if item.id == article.id:
                return
        abort(404)
    
    def _redirect_to_default(self, id):
        return self._redirect_to(
            controller='event', 
            action='show', 
            id=id
        )