# -*- coding: utf-8 -*-

from cStringIO import StringIO
from horosh import form, model
from horosh.lib.base import BaseController, render
from horosh.model import meta
from mimetypes import guess_type
from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
import string
import random
import Image
import logging
import os
import shutil

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
                avatar_url = self.relative_path(
                    avatar_source.filename.replace(os.sep, '_')
                ) 
                avatar_path = os.path.join(
                    config['app_conf']['permanent_store'],
                    avatar_url
                )
                dirname = os.path.dirname(avatar_path)
                if not os.path.isdir(dirname):
                    os.makedirs(dirname)
                avatar = Image.open(StringIO(avatar_source.value))
                avatar.thumbnail(THUMBNAIL_SIZE)
                avatar.save(avatar_path, "JPEG")

                node.avatar = avatar_url
                log.debug('node.avatar: %s' % node.avatar)
            
            node.node_user_id = session['current_user'].id
            
            meta.Session.add(node)
            event_node.members.append(node)
            meta.Session.commit()

            return self._redirect_to_default(event_node.id)
        
        c.form = fs
        c.fs = fs.fields
        return fs.render('/person/new.html', '/person/new_form.html', False)
    
    def edit(self, id, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)
        node = self._get_row(model.Person, id)
        fs = PersonForm('person-edit')
        
        if request.POST and fs.fields.cancel.id in request.POST:
            return self._redirect_to_default(event_node.id)

        if request.POST and fs.is_valid(request.POST):
            node.nickname = fs.fields.nickname.value
            node.fullname = fs.fields.fullname.value
            node.email = fs.fields.email.value

            if fs.fields.avatar.value is not None:
                avatar_source = fs.fields.avatar.value
                avatar_url = self.relative_path(
                    avatar_source.filename.replace(os.sep, '_')
                ) 
                avatar_path = os.path.join(
                    config['app_conf']['permanent_store'],
                    avatar_url
                )
                dirname = os.path.dirname(avatar_path)
                if not os.path.isdir(dirname):
                    os.makedirs(dirname)
                avatar = Image.open(StringIO(avatar_source.value))
                avatar.thumbnail(THUMBNAIL_SIZE)
                avatar.save(avatar_path, "JPEG")

                node.avatar = avatar_url
                log.debug('node.avatar: %s' % node.avatar)
            
            node.node_user_id = session['current_user'].id
            
            meta.Session.add(node)
            event_node.members.append(node)
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
        return fs.render('/person/edit.html', '/person/edit_form.html')
    
    def remove(self, id, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)
        node = self._get_row(model.Person, id)
        meta.Session.delete(node)
        meta.Session.commit()
        return self._redirect_to_default(event_node.id)
    
    def _redirect_to_default(self, id):
        return self._redirect_to(
            controller='event', 
            action='show', 
            id=id,
            event_id=None
        )

    def _check_access(self, node):
        if node.node_user_id != session['current_user'].id:
            abort(403)

    def relative_path(self, filename):
        """return the file path relative to root
        """
        rdir = lambda: ''.join(random.sample(string.ascii_lowercase, 8))
        path = '/'.join([rdir(), filename])
        return path
        