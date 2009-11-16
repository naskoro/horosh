# -*- coding: utf-8 -*-

from horosh import form, model
from horosh.lib.base import BaseController, render, is_ajax, current_user, redirect_to
from horosh.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort
import logging
import time

log = logging.getLogger(__name__)

DEFAULT_FILTER = 'reStrucuredText'

class ReportForm(form.FieldSet):
    def init(self):
        self.adds(
            form.Field('title', validator=form.v.String()),
            form.Field('content', validator=form.v.String(not_empty=True)),
            form.Field('save'),
            form.Field('cancel')
        )
    
class ReportController(BaseController):
    def new(self, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)
        
        fs = ReportForm('report-new')

        if request.POST and fs.fields.cancel.id in request.POST:
            return redirect_to(event_node.url())
        
        if request.POST and fs.is_valid(request.POST):
            node = model.Report()
            node.title = fs.fields.title.value
            node.content = fs.fields.content.value
            node.filter = DEFAULT_FILTER
            node.event = event_node 
            node.node_user_id = current_user().id
            
            meta.Session.add(node)
            meta.Session.commit()
            
            return redirect_to(node.url())
        
        c.form = fs
        c.fs = fs.fields
        
        if is_ajax():
            result = render('/report/new_partial.html')
        else:
            result = render('/report/new.html')
        if request.POST:
            result = fs.htmlfill(result)
        return result

    def show(self, event_id, id):
        event_node = self._get_row(model.Event, event_id)
        
        node = event_node.report_by_number(id)
        if node is None:
            abort(404)
         
        c.node = node
        
        return render('/report/show.html')

    def edit(self, id, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)
        node = event_node.report_by_number(id)
        if node is None:
            abort(404)

        fs = ReportForm('report-edit')

        if request.POST and fs.fields.cancel.id in request.POST:
            if self.last_page():
                return redirect_to(**self.last_page())
            return redirect_to(node.url())

        if request.POST and fs.is_valid(request.POST):
            
            node.title = fs.fields.title.value
            node.content = fs.fields.content.value
            
            meta.Session.commit()
            return redirect_to(node.url())

        if not request.POST:
            fs.set_values({
                'title': node.title,
                'content': node.content
            })
        
        c.form = fs
        c.fs = fs.fields
        c.node = node
        
        if is_ajax():
            result = render('/report/edit_partial.html')
        else:
            result = render('/report/edit.html')
        return fs.htmlfill(result)


    def remove(self, id, event_id):
        event_node = self._get_row(model.Event, event_id)
        self._check_access(event_node)
        node = event_node.report_by_number(id)
        if node is None:
            abort(404)
        
        meta.Session.delete(node)
        meta.Session.commit()
        return redirect_to(event_node.url())
    
    def _event_has_report(self, event, report):
        for item in event.reports:
            if item.id == report.id:
                return
        abort(404)
    
    def _redirect_to_default(self, event_node, node = None):
        if node is None:
            return self._redirect_to(
                controller='event', 
                action='show', 
                id=event_node.id,
            )
            
        return self._redirect_to(
            controller='report', 
            action='show', 
            event_id=event_node.id,
            id = node.number,
        )