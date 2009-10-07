# -*- coding: utf-8 -*-

import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from horosh.lib.base import BaseController, render
from horosh.lib.util import rst2html
from horosh.model import meta
from horosh import model
from horosh import form

log = logging.getLogger(__name__)

fs = form.FieldSet('event',
    form.Field('title', validator=form.v.String(not_empty=True)),
    form.Field('start', 
        validator=form.v.DateConverter(
            not_empty=True, 
            month_style='dd/mm/yyyy'
        )
    ),
    form.Field('finish',         
        validator=form.v.DateConverter(
            not_empty=True, 
            month_style='dd/mm/yyyy'
        )
    ),
    form.Field('summary', validator=form.v.String())
)
class EventController(BaseController):
    def new(self):
        if request.POST and fs.is_valid(request.POST):
            node = model.Event()
            node.title = fs.title.value
            node.summary = fs.summary.value
            node.start = fs.start.value
            node.finish = fs.finish.value
            node.node_user_id = session['current_user'].id
            
            meta.Session.add(node)
            meta.Session.commit()
            return self._redirect_to_default(node.id)
        c.fs = fs
        return fs.render('/event/new.html', '/event/new_form.html', False)
    def show(self, id):
        c.node = self._get_row(model.Event, id)
        return render('/event/show.html')
    def _redirect_to_default(self, id):
        return self._redirect_to(controller='event', action='show', id=id)