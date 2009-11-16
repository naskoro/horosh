# -*- coding: utf-8 -*-

"""The base Controller API

Provides the BaseController class for subclassing.
"""
from authkit.authorize.pylons_adaptors import authorized
from authkit.permissions import HasAuthKitRole
from horosh import model
from horosh.lib import taconite
from horosh.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, redirect_to as redirect_to_
from pylons.templating import render_mako as render
from routes import url_for
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

def is_admin():
    return authorized(HasAuthKitRole('admin'))
    
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

def redirect_to(*args, **kwargs):
    if is_ajax():
        c.args = args
        c.kwargs = kwargs
        result = render('/util/redirect.html')
    else :
        redirect_to_(*args, **kwargs)
        result = "Moved temporarily"
    return result


class BaseController(WSGIController):
    def __before__(self):
        current = request.environ['pylons.routes_dict']
        if 'page_current' in session and session['page_current'] != current:
            session['last_page'] = session['page_current']
            
        session['page_current'] =  current
        session.save()
         
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
    
    def last_page(self):
        if 'last_page' in session:
            return session['last_page']
        return None

    def _redirect_to(self, *args, **kwargs):
        return redirect_to(*args, **kwargs)
    
    def _get_row(self, model, id):
        try:
            row = meta.Session.query(model).filter_by(id=int(id)).one()
        except NoResultFound:
            abort(404)
        return row

    def _check_access(self, node):
        if not is_node_owner(node):
            abort(403)            