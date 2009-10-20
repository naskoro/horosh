# -*- coding: utf-8 -*-

from horosh.lib.base import BaseController, render
from horosh.lib.util import rst2html
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators.rest import restrict
from webhelpers.markdown import markdown
from mimetypes import guess_type
import logging

log = logging.getLogger(__name__)

class UtilController(BaseController):

    @restrict('POST')
    def markdown(self):
        text = request.POST['data'] 
        if text is None:
            abort(400)
        c.content = markdown(text)     
        return render('/util/response.html')

    @restrict('POST')
    def rst(self):
        text = request.POST['data'] 
        if c.content is None:
            abort(400)
        text = rst2html(text)
        c.content = text     
        return render('/util/response.html')
    
    def flash_file(self, id):
        if id in session['flash_file']:
            file =  session['flash_file'][id];
        else:
            abort(404)
        data = file['content']
        response.content_type = guess_type(file['filename'])[0] or 'text/plain'
        return data
