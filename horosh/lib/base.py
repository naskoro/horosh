# -*- coding: utf-8 -*-

"""The base Controller API

Provides the BaseController class for subclassing.
"""
from horosh import model
from horosh.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, redirect_to
from pylons.templating import render_mako as render
from sqlalchemy.orm.exc import NoResultFound
import logging

log = logging.getLogger(__name__)

class BaseController(WSGIController):
    def __before__(self):
        if 'current_user' not in session:
            session['current_user'] = meta.Session.query(model.User).filter_by(email='naspeh@pusto.org').one()
            session.save()
    
    def __after__(self):
        if self.is_ajax():
            response.content_type = 'text/xml'
               
    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()
    
    def is_ajax(self):
        return request.is_xhr or 'is_ajax' in request.params
    
    def _redirect_to(self, **url):
        if request.is_xhr or 'is_ajax' in request.params:
            c.url = url
            result = render('/util/redirect.html')
        else :
            redirect_to(**url)
            result = "Moved temporarily"
        return result
    
    def _get_row(self, model, id):
        try:
            row = meta.Session.query(model).filter_by(id=int(id)).one()
        except NoResultFound:
            abort(404)
        return row