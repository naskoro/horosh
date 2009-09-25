# -*- coding: utf-8 -*-

import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from horosh.lib.base import BaseController, render
from horosh.lib.util import getCurrentUser
from horosh.model import meta
from horosh import model
from horosh import form

log = logging.getLogger(__name__)

EventForm = form.FieldSet(model.Event)
EventForm.configure(
    include=[
        EventForm.title,
        EventForm.summary.textarea(),
        EventForm.start,
        EventForm.finish,
        EventForm.published
    ])

class EventController(BaseController):

    def new(self, id=None):
        if id:
            record = meta.Session.query(model.Event).filter_by(id=id).first()
            log.debug(record)
        else:
            record = model.Event()
        assert record is not None, repr(id)        
        c.fs = EventForm.bind(record, data=request.POST or None)
        if request.POST and c.fs.validate():
            c.fs.sync()
            if id:
                meta.Session.update(record)
            else:
                record.node_user_id = getCurrentUser().id
                meta.Session.add(record)
            meta.Session.commit()
            redirect_to(id=record.id)        
        return render('/event/new.html')