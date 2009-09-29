"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
import logging
from webhelpers.html.tags import *
from routes import url_for

from horosh.lib.photos import Picasa              