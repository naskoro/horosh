"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.controllers.util import redirect_to
from pylons.templating import render_mako as render
from pylons import request

from horosh.model import meta

class BaseController(WSGIController):

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