# -*- coding: utf-8 -*-

from horosh import form, model
from horosh.lib.base import BaseController, render
from horosh.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
import logging

log = logging.getLogger(__name__)

class EventForm(form.FieldSet):
    def init(self):
        self.adds(
            form.Field('category', validator=form.v.String(not_empty=True)),
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
        fs = EventForm('event-new')
        if request.POST and fs.is_valid(request.POST):
            node = model.Event()
            node.category = fs.fields.category.value
            node.title = fs.fields.title.value
            node.summary = fs.fields.summary.value
            node.start = fs.fields.start.value
            node.finish = fs.fields.finish.value
            node.node_user_id = session['current_user'].id
            
            meta.Session.add(node)
            meta.Session.commit()
            return self._redirect_to_default(node.id)
        
        c.form = fs
        c.fs = fs.fields
        return fs.render('/event/new.html', '/event/new_form.html', False)
    
    def show(self, id):
        c.node = self._get_row(model.Event, id)
        return render('/event/show.html')
    
    def _redirect_to_default(self, id):
        return self._redirect_to(controller='event', action='show', id=id)