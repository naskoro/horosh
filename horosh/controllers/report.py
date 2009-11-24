# -*- coding: utf-8 -*-

from horosh import form, model
from horosh.lib.base import BaseController, render, redirect_to, flash, \
    is_ajax, current_user
from horosh.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort
import logging

log = logging.getLogger(__name__)

class ReportForm(form.FieldSet):
    def init(self):
        self.adds(
            form.Field('title', validator=form.v.String()),
            form.Field('content', validator=form.v.String(not_empty=True)),
            form.Field('save'),
            form.Field('save_view'),
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
            node.event = event_node
            node.node_user_id = current_user().id

            meta.Session.add(node)
            meta.Session.commit()
            flash(u'Отчет успешно добавлен')
            if fs.fields.save_view.id in request.POST:
                return redirect_to(node.url())
            else:
                return redirect_to(event_node.url())


        c.form = fs
        c.fs = fs.fields

        if is_ajax():
            result = render('/report/new_partial.html')
        else:
            result = render('/report/new.html')
        if request.POST:
            result = fs.htmlfill(result)
        return result

    def show(self, id):
        self.is_page_back = True

        node = self._get_row(model.Report, id)
        event_node = node.event
        self._check_access(event_node)

        c.node = node

        return render('/report/show.html')

    def edit(self, id):
        node = self._get_row(model.Report, id)
        event_node = node.event
        self._check_access(event_node)

        fs = ReportForm('report-edit')

        if request.POST and fs.fields.cancel.id in request.POST:
            if self.back_page():
                return redirect_to(**self.back_page())
            return redirect_to(node.url())

        if request.POST and fs.is_valid(request.POST):

            node.title = fs.fields.title.value
            node.content = fs.fields.content.value

            meta.Session.commit()
            flash(u'Отчет успешно сохранен')
            if fs.fields.save_view.id in request.POST:
                return redirect_to(node.url())
            else:
                return redirect_to(event_node.url())

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


    def remove(self, id):
        node = self._get_row(model.Report, id)
        event_node = node.event
        self._check_access(event_node)

        meta.Session.delete(node)
        meta.Session.commit()
        flash(u'Отчет успешно удален')
        return redirect_to(event_node.url())
