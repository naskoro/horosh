# -*- coding: utf-8 -*-

from cStringIO import StringIO
from horosh import form, model
from horosh.lib.base import BaseController, render, is_ajax, current_user
from horosh.model import meta
from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
import Image
import logging
import os.path
import time

log = logging.getLogger(__name__)

THUMBNAIL_SIZE = 100, 100
NO_AVATAR = 'images/no-avatar.png'

class PersonForm(form.FieldSet):
    def init(self):
        self.adds(
            form.Field('fullname', validator=form.v.String(not_empty=True, min=3, max=30)),
            form.Field('avatar', validator=form.v.ImageUploadValidator(not_empty=True, max=3072)),
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
            node.fullname = fs.fields.fullname.value
            node.event = event_node
            
            if fs.fields.avatar.value is not None:
                node.avatar = self._avatar_prepare(fs.fields.avatar.value.file)
            
            node.node_user_id = current_user().id
            
            meta.Session.add(node)
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
            node.fullname = fs.fields.fullname.value

            if fs.fields.avatar.value is not None:
                node.avatar = self._avatar_prepare(fs.fields.avatar.value.file)
            
            meta.Session.add(node)
            event_node.persons.append(node)
            meta.Session.commit()

            return self._redirect_to_default(event_node.id)
        
        if not request.POST:
            fs.set_values({
                'fullname': node.fullname,
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

    def avatar(self, id):
        node = self._get_row(model.Person, id)
        response.content_type = 'image/png'
        
        if node.avatar is None: 
            filename = os.path.join(
                config['app_conf']['public_dir'],
                NO_AVATAR
            )
            if not os.path.exists(filename):
                return 'No such file'
            permanent_file = open(filename, 'rb')
            data = permanent_file.read()
            permanent_file.close()
            return data
        
        response.expires = 'Mon, 26 Jul 1990 05:00:00 GMT'
        response.last_modified = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
        response.cache_control = 'no-cache, must-revalidate'
        response.pragma = 'no-cache' 
        return node.avatar
    
    def _avatar_prepare(self, avatar):
        pic = Image.open(avatar)
        pic.thumbnail(THUMBNAIL_SIZE)
        buffer = StringIO()
        pic.save(buffer, pic.format)
        buffer.seek(0)
        return buffer.read()
    
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