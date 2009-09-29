# -*- coding: utf-8 -*-

from pylons.controllers import WSGIController
from pylons.controllers.util import redirect_to
from pylons import request, response, session, tmpl_context as c

from horosh.model import meta
from horosh import model

class BaseController(WSGIController):
    def __before__(self):
            session.current_user = meta.Session.query(model.User).filter_by(email='naspeh@pusto.org').one()

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()
    
    def _redirect_to(self, **url):
        if (request.is_xhr):
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