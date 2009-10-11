# -*- coding: utf-8 -*-

from horosh import form, model
from horosh.lib.base import BaseController, render
from horosh.lib.util import rst2html
from horosh.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
import logging
import time



log = logging.getLogger(__name__)

class ArticleForm(form.FieldSet):
    def init(self):
        self.adds(
            form.Field('title', validator=form.v.String(not_empty=True)),
            form.Field('album_user', validator=form.v.String()),
            form.Field('album_id', validator=form.v.String()),
            form.Field('content', validator=form.v.String(not_empty=True))
        )
    
class ArticleController(BaseController):
    def new(self):
        fs = ArticleForm('article-new')
        if request.POST and fs.is_valid(request.POST):
            node = model.Article()
            node.title = fs.fields.title.value
            node.content = fs.fields.content.value
            node.filter = 'reStrucuredText'
            node.html_content = rst2html(node.content)
            node.node_user_id = session['current_user'].id
            
            meta.Session.add(node)
            meta.Session.commit()
            return self._redirect_to_default(node.id)
        c.fs = fs.fields
        return fs.render('/article/new.html', '/article/new_form.html', False)

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
    
    def _redirect_to_default(self, id):
        return self._redirect_to(controller='article', action='show', id=id)