# -*- coding: utf-8 -*-

"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from horosh.lib.base import is_ajax, on_page
from horosh.lib.photos import picasa_by_data, picasa_by_user
from horosh.lib.util import rst2html
from routes import url_for
from webhelpers.html.tags import *
from webhelpers.text import *
import logging
import time

log = logging.getLogger(__name__)