# -*- coding: utf-8 -*-

from horosh import form, model
from horosh.lib import picasa
from horosh.lib.base import BaseController, render, redirect_to, is_ajax, \
    current_user, is_admin, flash
from horosh.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort
from urllib import urlopen
import gdata
import logging

log = logging.getLogger(__name__)

class AlbumForm(form.FieldSet):
    def init(self):
        self.adds(
            form.Field('user', validator=form.v.PicasaUser(not_empty=True, min=6, max=30)),
            form.Field('albumid', validator=form.v.String(not_empty=True)),
            form.Field('save'),
            form.Field('cancel')

        )
        self.schema.chained_validators = [form.v.PicasaAlbum('user', 'albumid')]

class AlbumController(BaseController):
    def new(self, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)

        fs = AlbumForm('album-new')

        if request.POST and fs.fields.cancel.id in request.POST:
            return redirect_to(event_node.url())

        if request.POST and fs.is_valid(request.POST):
            node = model.Album()
            node.settings = picasa.photos(fs.fields.user.value, fs.fields.albumid.value, limit=30)
            node.node_user_id = current_user().id

            meta.Session.add(node)
            event_node.albums.append(node)
            meta.Session.commit()
            flash(u'Альбом успешно добавлен')
            return redirect_to(event_node.url())

        c.form = fs
        c.fs = fs.fields

        if is_ajax():
            result = render('/album/new_partial.html')
        else:
            result = render('/album/new.html')
        if request.POST:
            result = fs.htmlfill(result)
        return result

    def reload(self, id, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)
        node = self._get_row(model.Album, id)
        self._event_has_album(event_node, node)
        
        album = gdata.GDataFeedFromString(node.settings)
        node.settings = urlopen(album.GetSelfLink().href).read()
        
        meta.Session.commit()
        flash(u'Альбом успешно обновлен')
        return redirect_to(event_node.url())

    def remove(self, id, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)
        node = self._get_row(model.Album, id)
        self._event_has_album(event_node, node)

        meta.Session.delete(node)
        meta.Session.commit()
        flash(u'Альбом успешно удален')
        return redirect_to(event_node.url())

    def _event_has_album(self, event, album):
        for item in event.albums:
            if item.id == album.id:
                return
        abort(404)
