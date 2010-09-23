# -*- coding: utf-8 -*-
import logging
from urllib import urlopen

import gdata
from pylons import request, tmpl_context as c

from horosh import form, model
from horosh.lib import picasa
from horosh.lib.base import (
    BaseController, render, redirect_to, flash, is_ajax, current_user
)
from horosh.model import meta


log = logging.getLogger(__name__)


class AlbumForm(form.FieldSet):
    def init(self):
        self.adds(
            form.Field('user',
                validator=form.v.PicasaUser(not_empty=True, min=6, max=30)
            ),
            form.Field('albumid', validator=form.v.String(not_empty=True)),
            form.Field('save'),
            form.Field('cancel')

        )
        self.schema.chained_validators = [
            form.v.PicasaAlbum('user', 'albumid')
        ]


class AlbumController(BaseController):
    def show(self, id, gallery_id):
        node = self._get_row(model.Album, id)
        c.photos = picasa.photos_by_album(node)
        c.id = gallery_id
        return render('/album/show.html')

    def new(self, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)

        fs = AlbumForm('album-new')

        if request.POST and fs.fields.cancel.id in request.POST:
            return redirect_to(event_node.url())

        if request.POST and fs.is_valid(request.POST):
            node = model.Album()
            node.settings = picasa.photos(
                fs.fields.user.value, fs.fields.albumid.value, limit=30
            )
            node.node_user_id = current_user().id

            meta.Session.add(node)
            event_node.albums.append(node)
            meta.Session.commit()
            flash(u'Альбом успешно добавлен')
            if self.back_page():
                return redirect_to(**self.back_page())
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

    def reload(self, id):
        node = self._get_row(model.Album, id)
        event_node = node.event
        self._check_access(event_node)

        album = gdata.GDataFeedFromString(node.settings)
        node.settings = urlopen(album.GetSelfLink().href).read()

        meta.Session.commit()
        flash(u'Альбом успешно обновлен')
        if self.back_page():
                return redirect_to(**self.back_page())
        return redirect_to(event_node.url())

    def remove(self, id):
        node = self._get_row(model.Album, id)
        event_node = node.event
        self._check_access(event_node)

        fs = form.DeleteAcceptForm('album-remove')

        if request.POST:
            if fs.fields.save.id in request.POST:
                meta.Session.delete(node)
                meta.Session.commit()
                flash(u'Альбом успешно удален')
            if self.back_page():
                return redirect_to(**self.back_page())
            return redirect_to(event_node.url())
        else:
            c.form = fs
            if is_ajax():
                result = render('/util/delete_accept_partial.html')
            else:
                result = render('/util/delete_accept.html')
            return result
