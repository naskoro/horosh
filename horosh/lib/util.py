# -*- coding: utf-8 -*-

from docutils.core import publish_parts
from mako.template import Template
from pylons.templating import pylons_globals
from webhelpers.text import truncate
from html5lib import treebuilders
import html5lib
import logging

log = logging.getLogger(__name__)

def rst2html(text, use_ext=True):
    text = publish_parts(
        text, 
        writer_name='html',
        settings_overrides=dict(file_insertion_enabled=False, raw_enabled=False)
    )
    result = text['html_body']
    if use_ext:
        globs = pylons_globals()
        template = Template(result)
        result = template.render_unicode(**globs)
        
    return result

def truncate_html(*args):
    document = truncate(*args) 
    parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))
    document = parser.parse(document)
    
    xml = document.getElementsByTagName('body')[0].childNodes[0].toxml()
    return xml

def human_filesize(size):
    for x in ['bytes','KB','MB','GB','TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
