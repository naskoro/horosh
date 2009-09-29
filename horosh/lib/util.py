# -*- coding: utf-8 -*-

from docutils.core import publish_parts
from pylons.templating import pylons_globals
from mako.template import Template

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