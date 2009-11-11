# -*- coding: utf-8 -*-

"""The base Controller API

Provides the BaseController class for subclassing.
"""
from horosh import model
from horosh.lib import taconite
from horosh.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, redirect_to
from pylons.templating import render_mako as render
from sqlalchemy.orm.exc import NoResultFound
import logging

log = logging.getLogger(__name__)
def is_ajax():
    return request.is_xhr or 'is_ajax' in request.params

def on_page():
    return 'on_page' in request.params and is_ajax()

def is_node_owner(node):
    if node.node_user_id == current_user().id:
        return True
    return False

def authkit_user():
    if not request.environ.get('REMOTE_USER'):
        user = 'nobody'
    else:
        user = request.environ.get('REMOTE_USER')
    return user

def current_user():
    if not request.environ.get('current_user'):
        user = meta.Session.query(model.User).filter_by(nickname=authkit_user).one()
        request.environ['current_user'] = user
    return request.environ.get('current_user')

class BaseController(WSGIController):
    def __after__(self):
        if is_ajax():
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
    
    def taconite(self, xhtml):
        return render('/util/taconite.html', {
                'xhtml': taconite.clean(xhtml),
                'scripts': taconite.scripts(xhtml),
            })
    
    def _redirect_to(self, *args, **kwargs):
        if is_ajax():
            c.args = args
            c.kwargs = kwargs
            result = render('/util/redirect.html')
        else :
            redirect_to(*args, **kwargs)
            result = "Moved temporarily"
        return result
    
    def _get_row(self, model, id):
        try:
            row = meta.Session.query(model).filter_by(id=int(id)).one()
        except NoResultFound:
            abort(404)
        return row

    def _check_access(self, node):
        if not is_node_owner(node):
            abort(403)            