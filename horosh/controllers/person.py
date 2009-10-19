# -*- coding: utf-8 -*-

from horosh import form, model
from horosh.lib.base import BaseController, render
from horosh.model import meta
from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from mimetypes import guess_type
import logging
import os
import shutil

log = logging.getLogger(__name__)

class PersonForm(form.FieldSet):
    def init(self):
        self.adds(
            form.Field('nickname', validator=form.v.String(not_empty=False, min=3, max=20)),
            form.Field('fullname', validator=form.v.String(not_empty=True, min=3, max=30)),
            form.Field('email', validator=form.v.Email()),
            form.Field('avatar', validator=form.v.String()),
        )

class PersonController(BaseController):
    
    def new(self, node_id):
        parent_node = self._get_row(model.Node, node_id)
        fs = PersonForm('person-new')
        avatar_result = None
        if request.POST:
            if request.POST and fs.fields.avatar.id in request.POST and request.POST[fs.fields.avatar.id]:
                avatar = request.POST[fs.fields.avatar.id]
                log.debug(avatar)
                log.debug(guess_type(avatar.filename)[0])
                avatar_result = open(
                    os.path.join(
                        config['app_conf']['permanent_store'],
                        avatar.filename.replace(os.sep, '_')
                    ),
                    'wb'
                )
                shutil.copyfileobj(avatar.file, avatar_result)
                avatar.file.close()
                avatar_result.close()
            
            if fs.is_valid(request.POST):
                node = model.Person()
                node.nickname = fs.fields.nickname.value
                node.fullname = fs.fields.fullname.value
                node.email = fs.fields.email.value
                if avatar_result is not None:
                    node.avatar = avatar_result.name
                elif fs.fields.avatar.id in session:
                    node.avatar = session[fs.fields.avatar.id].name
                log.debug('node.avatar: %s' % node.avatar)
                node.node_user_id = session['current_user'].id
                
                #meta.Session.add(node)
                #meta.Session.commit()
                return self._redirect_to(
                    controller=parent_node.node_type, 
                    action='show', 
                    id=parent_node.id
                )
            elif avatar_result is not None:
                session[fs.fields.avatar.id] = avatar_result
                session.save()
        elif fs.fields.avatar.id in session:
            del session[fs.fields.avatar.id]
            session.save()
        c.form = fs
        c.fs = fs.fields
        return fs.render('/person/new.html', '/person/new_form.html', False)
    def show(self):
        return "Person Show"
    def _redirect_to_default(self, node):
        return     