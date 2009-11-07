# -*- coding: utf-8 -*-

from horosh import form, model
from horosh.lib.base import BaseController, render, is_ajax
from horosh.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
import logging

log = logging.getLogger(__name__)

DATE_FORMAT = '%d/%m/%Y'
MONTH_STYLE = 'dd/mm/yyyy' # 'dd/mm/yyyy' or 'mm/dd/yyyy' 

class EventForm(form.FieldSet):
    def init(self):
        self.adds(
            form.Field('category', validator=form.v.String(not_empty=True)),
            form.Field('title', validator=form.v.String(not_empty=True)),
            form.Field('start', 
                validator=form.v.DateConverter(
                    not_empty=True, 
                    month_style=MONTH_STYLE
                )
            ),
            form.Field('finish',         
                validator=form.v.DateConverter(
                    not_empty=True, 
                    month_style=MONTH_STYLE
                )
            ),
            form.Field('summary', validator=form.v.String()),
            form.Field('save'),
            form.Field('cancel')
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
        
        if is_ajax():
            result = render('/event/new_partial.html')
        else:
            result = render('/event/new.html')
        if request.POST:
            result = fs.htmlfill(result)
        return result
    
    def edit(self, id):
        node = self._get_row(model.Event, id)
        self._check_access(node)
        
        fs = EventForm('event-edit')
        
        if request.POST and fs.fields.cancel.id in request.POST:
            return self._redirect_to_default(node.id)

        if request.POST and fs.is_valid(request.POST):
            node.category = fs.fields.category.value
            node.title = fs.fields.title.value
            node.summary = fs.fields.summary.value
            node.start = fs.fields.start.value
            node.finish = fs.fields.finish.value
            
            meta.Session.commit()

            return self._redirect_to_default(node.id)
        
        if not request.POST:
            fs.set_values({
                'category': node.category,
                'title': node.title,
                'start': node.start.strftime(DATE_FORMAT),
                'finish': node.finish.strftime(DATE_FORMAT),
                'summary': node.summary
            })

        c.node = node
        c.form = fs
        c.fs = fs.fields
        
        if is_ajax():
            result = render('/event/edit_partial.html')
        else:
            result = render('/event/edit.html')
        return fs.htmlfill(result)
    
    def show(self, id):
        c.node = self._get_row(model.Event, id)
        
        if is_ajax():
            result = self.taconite(render('/event/show_partial.html'))
            #result = render('/event/show_partial.html')
        else:
            result = render('/event/show.html')
        return result

    def remove(self, id):
        node = self._get_row(model.Event, id)
        self._check_access(node)
        
        meta.Session.delete(node)
        meta.Session.commit()
        return self._redirect_to(controller='event', action='new')

    def _redirect_to_default(self, id):
        return self._redirect_to(controller='event', action='show', id=id)