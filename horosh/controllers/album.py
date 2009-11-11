# -*- coding: utf-8 -*-

from horosh import form, model
from horosh.lib.base import BaseController, render, is_ajax, current_user
from horosh.lib.photos import Picasa
from horosh.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
import logging

log = logging.getLogger(__name__)

class AlbumForm(form.FieldSet):
    def init(self):
        self.adds(
            form.Field('user', validator=form.v.String(not_empty=True, min=6, max=30)),
            form.Field('albumid', validator=form.v.String(not_empty=True)),
            form.Field('save'),
            form.Field('cancel')
            
        )
        self.schema.chained_validators = [form.v.PicasaAlbumValidator('user', 'albumid')]

class AlbumController(BaseController):
    def new(self, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)
        
        fs = AlbumForm('album-new')

        if request.POST and fs.fields.cancel.id in request.POST:
            return self._redirect_to_default(event_node.id)
        
        if request.POST and fs.is_valid(request.POST):
            album = Picasa()
            
            node = model.Album()
            node.settings = album.photos(fs.fields.user.value, fs.fields.albumid.value, limit=30)
            node.node_user_id = current_user().id
            
            meta.Session.add(node)
            event_node.albums.append(node)
            meta.Session.commit()

            return self._redirect_to_default(event_node.id)
        
        c.form = fs
        c.fs = fs.fields
        
        if is_ajax():
            result = render('/album/new_partial.html')
        else:
            result = render('/album/new.html')
        if request.POST:
            result = fs.htmlfill(result)
        return result
    
    def edit(self, id, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)
        node = self._get_row(model.Album, id)
        self._event_has_album(event_node, node)
        
        fs = AlbumForm('album-edit')
        
        if request.POST and fs.fields.cancel.id in request.POST:
            return self._redirect_to_default(event_node.id)

        if request.POST and fs.is_valid(request.POST):
            album = Picasa()
            
            node = model.Album()
            node.settings = album.photos(fs.fields.user.value, fs.fields.albumid.value, limit=30)
            
            meta.Session.commit()

            return self._redirect_to_default(event_node.id)
        
        if not request.POST:
            fs.set_values({
            })

        c.node = node
        c.form = fs
        c.fs = fs.fields
        
        if is_ajax():
            result = render('/album/edit_partial.html')
        else:
            result = render('/album/edit.html')
        return fs.htmlfill(result)
    
    def remove(self, id, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)
        node = self._get_row(model.Album, id)
        self._event_has_album(event_node, node)
        
        meta.Session.delete(node)
        meta.Session.commit()
        return self._redirect_to_default(event_node.id)

    def _event_has_album(self, event, album):
        for item in event.albums:
            if item.id == album.id:
                return
        abort(404)
    
    def _redirect_to_default(self, id):
        return self._redirect_to(
            controller='event', 
            action='show', 
            id=id
        )
