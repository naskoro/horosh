# -*- coding: utf-8 -*-

import logging

import formencode as form
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import restrict

from horosh.lib.base import BaseController, render
from horosh.lib.util import getCurrentUser
from horosh.model import meta
from horosh import model

log = logging.getLogger(__name__)
class PicasaForm(form.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    album_picasa_username = form.validators.String(
        not_empty=True,
        messages={}
    )
    album_picasa_albumid = form.validators.String(
        not_empty=True,
        messages={}
    )

class AlbumController(BaseController):

    def new_picasa(self):
        return render('/album/new_picasa.html')

    @restrict('POST')
    @validate(schema=PicasaForm(), form='new_picasa')
    def create_picasa(self):
        data = {}
        data['username'] = self.form_result['album_picasa_username']
        data['albumid'] = self.form_result['album_picasa_albumid']
        data['node_user_id'] = getCurrentUser().id
        node = model.Article(**data)
        meta.Session.add(node)
        meta.Session.commit()
        return self._redirectToDefault(node.id)

    def _redirectToDefault(self, id):
        url = {'controller': 'album', 'action': 'show_picasa', 'id': id}
        log.info(dir(url))
        if (request.is_xhr):
            c.url = url
            result = render('/util/redirect.html')
        else :
            redirect_to(**url)
            result = "Moved temporarily"  
        return result