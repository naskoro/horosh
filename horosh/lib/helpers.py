"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from horosh.lib.photos import Picasa
from horosh.lib.base import is_ajax
from routes import url_for
from webhelpers.html.tags import *
import logging