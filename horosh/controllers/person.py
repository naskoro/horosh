# -*- coding: utf-8 -*-

from horosh import form, model
from horosh.lib.base import BaseController, render, is_ajax
from horosh.lib.photos import Photo
from horosh.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
import logging

log = logging.getLogger(__name__)

THUMBNAIL_SIZE = 100, 100

class PersonForm(form.FieldSet):
    def init(self):
        self.adds(
            form.Field('nickname', validator=form.v.String(not_empty=False, min=3, max=20)),
            form.Field('fullname', validator=form.v.String(not_empty=True, min=3, max=30)),
            form.Field('email', validator=form.v.Email()),
            form.Field('avatar', validator=form.v.ImageUploadValidator()),
            form.Field('save'),
            form.Field('cancel')
        )


class PersonController(BaseController):
    def new(self, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)
        
        fs = PersonForm('person-new')

        if request.POST and fs.fields.cancel.id in request.POST:
            return self._redirect_to_default(event_node.id)
        
        if request.POST and fs.is_valid(request.POST):
            node = model.Person()
            node.nickname = fs.fields.nickname.value
            node.fullname = fs.fields.fullname.value
            node.email = fs.fields.email.value

            if fs.fields.avatar.value is not None:
                avatar_source = fs.fields.avatar.value
                photo = Photo(avatar_source.filename, avatar_source.value)
                node.avatar = photo.thumbnail_url(THUMBNAIL_SIZE)
            
            node.node_user_id = session['current_user'].id
            
            meta.Session.add(node)
            event_node.persons.append(node)
            meta.Session.commit()

            return self._redirect_to_default(event_node.id)
        
        c.form = fs
        c.fs = fs.fields
        
        if is_ajax():
            result = render('/person/new_partial.html')
        else:
            result = render('/person/new.html')
        if request.POST:
            result = fs.htmlfill(result)
        return result
    
    def edit(self, id, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)
        node = self._get_row(model.Person, id)
        self._event_has_person(event_node, node)
        
        fs = PersonForm('person-edit')
        
        if request.POST and fs.fields.cancel.id in request.POST:
            return self._redirect_to_default(event_node.id)

        if request.POST and fs.is_valid(request.POST):
            node.nickname = fs.fields.nickname.value
            node.fullname = fs.fields.fullname.value
            node.email = fs.fields.email.value

            if fs.fields.avatar.value is not None:
                avatar_source = fs.fields.avatar.value
                photo = Photo(avatar_source.filename, avatar_source.value)
                node.avatar = photo.thumbnail_url(THUMBNAIL_SIZE)
            
            node.node_user_id = session['current_user'].id
            
            meta.Session.add(node)
            event_node.persons.append(node)
            meta.Session.commit()

            return self._redirect_to_default(event_node.id)
        
        if not request.POST:
            fs.set_values({
                'nickname': node.nickname,
                'fullname': node.fullname,
                'email': node.email,
                'avatar': node.avatar
            })

        c.node = node
        c.form = fs
        c.fs = fs.fields
        
        if is_ajax():
            result = render('/person/edit_partial.html')
        else:
            result = render('/person/edit.html')
        return fs.htmlfill(result)
    
    def remove(self, id, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)
        node = self._get_row(model.Person, id)
        self._event_has_person(event_node, node)
        
        meta.Session.delete(node)
        meta.Session.commit()
        return self._redirect_to_default(event_node.id)

    def _event_has_person(self, event, person):
        for item in event.persons:
            if item.id == person.id:
                return
        abort(404)
    
    def _redirect_to_default(self, id):
        return self._redirect_to(
            controller='event', 
            action='show', 
            id=id
        )