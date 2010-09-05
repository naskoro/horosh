# -*- coding: utf-8 -*-
"""
The base Controller API

Provides the BaseController class for subclassing.
"""
import logging
import re

from authkit.authorize.pylons_adaptors import authorized
from authkit.permissions import HasAuthKitRole, ValidAuthKitUser
from pylons import request, response, session, tmpl_context as c
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, redirect_to as _redirect_to
from pylons.templating import render_mako
from routes import url_for
from sqlalchemy.orm.exc import NoResultFound
from webhelpers import paginate
from webhelpers.pylonslib import Flash as _Flash

from horosh import model
from horosh.lib import taconite
from horosh.model import meta


log = logging.getLogger(__name__)

flash = _Flash()

def current_user():
    if not request.environ.get('current_user'):
        user = meta.Session.query(model.User).filter_by(nickname=remote_user).one()
        request.environ['current_user'] = user
    return request.environ.get('current_user')

def is_ajax():
    return request.is_xhr or 'is_ajax' in request.params

def on_page():
    return 'on_page' in request.params and is_ajax()

def is_node_owner(node):
    return is_authorized() and (node.node_user_id == current_user().id or is_admin()) or False

def is_authorized():
    return authorized(ValidAuthKitUser())

def is_admin():
    return authorized(HasAuthKitRole('admin'))

def is_nobody():
    return remote_user() == 'nobody'

def remote_user():
    if not request.environ.get('REMOTE_USER'):
        user = 'nobody'
    else:
        user = request.environ.get('REMOTE_USER')
    return user

def render(*args, **kwargs):
    if is_ajax():
        c.flash_messages += flash.pop_messages()
    return render_mako(*args, **kwargs)

def redirect_to(*args, **kwargs):
    if is_ajax():
        url = url_for(*args, **kwargs)
        c.url = url
        result = render('/util/redirect.html')
    else :
        _redirect_to(*args, **kwargs)
        result = "Moved temporarily"
    return result

def pager_or_404(query, items_per_page=10):
    page = request.params.get('page', None)
    if 'all' == page:
        nodes = query.all()
    else:
        if page and re.search('\D', page):
            abort(404)

        nodes = paginate.Page(
            query,
            page= page and int(page) or 1,
            items_per_page = items_per_page,
            **request.environ['pylons.routes_dict']
        )
    return nodes





class BaseController(WSGIController):
    def __before__(self):
        self.is_page_back = False
        c.flash_messages = flash.pop_messages()
        c.current_user=current_user()

    def __after__(self):
        if self.is_page_back:
            session['back_page'] = request.environ['pylons.routes_dict']
            session.save()

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

    def back_page(self):
        if 'back_page' in session:
            return session['back_page']
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
