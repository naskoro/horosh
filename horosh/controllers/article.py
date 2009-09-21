# -*- coding: utf-8 -*-

import logging

import formencode
from formencode import htmlfill
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import restrict
from webhelpers.markdown import markdown

from horosh.lib.base import BaseController, render
from horosh.lib.utils import rest2html

log = logging.getLogger(__name__)

class ContentForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    title = formencode.validators.String(
        not_empty=True,
        messages={}
    )
    content = formencode.validators.String(
        not_empty=True,
        messages={}
    )
    
class ArticleController(BaseController):

    def edit(self, id):
        return render('/article/edit.html')
    
    def new(self):
        return render('/article/new.html')

    @restrict('POST')
    @validate(schema=ContentForm(), form='new')
    def create(self):
        # Add the new content to the database
        content = model.Content()
        for k, v in self.form_result.items():
            setattr(content, k, v)
        meta.Session.add(content)
        meta.Session.commit()
        # Issue an HTTP redirect
        response.status_int = 302
        response.headers['location'] = h.url_for(controller='content',
            action='view', id=content.id)
        return "Moved temporarily"
    
    def show(self):
        text = """
A ReStructuredText Primer
=========================

:Author: Richard Jones
:Version: $Revision: 5801 $
:Copyright: This document has been placed in the public domain.

.. contents::


The text below contains links that look like "(quickref__)".  These
are relative links that point to the `Quick reStructuredText`_ user
reference.  If these links don't work, please refer to the `master
quick reference`_ document.

__
.. _Quick reStructuredText: quickref.html
.. _master quick reference:
   http://docutils.sourceforge.net/docs/user/rst/quickref.html

.. Note:: This document is an informal introduction to
   reStructuredText.  The `What Next?` section below has links to
   further resources, including a formal reference.

Lorem ipsum [#f1]_ dolor sit amet ... [#f2]_

.. rubric:: Footnotes

.. [#f1] Text of the first footnote.
.. [#f2] Text of the second footnote.

"""
        c.content = rest2html(text)
    
        return render('/article/show.html')