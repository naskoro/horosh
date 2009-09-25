# -*- coding: utf-8 -*-

import logging
from pylons import config
from formalchemy import config as fa_config
from formalchemy.ext.fsblob import FileFieldRenderer
from formalchemy.ext.fsblob import ImageFieldRenderer
from formalchemy import templates

from horosh.lib.base import render

log = logging.getLogger(__name__)

def __init__():
    log.debug(config.keys())
    if 'storage_path' in config['app_conf']:
        # set the storage_path if we can find an options in app_conf
        FileFieldRenderer.storage_path = config['app_conf']['storage_path']
        ImageFieldRenderer.storage_path = config['app_conf']['storage_path']
    
    fa_config.encoding = 'utf-8'
    
    class TemplateEngine(templates.TemplateEngine):
        def render(self, name, **kwargs):
            return render('/forms/%s.html' % name, extra_vars=kwargs)
    fa_config.engine = TemplateEngine()