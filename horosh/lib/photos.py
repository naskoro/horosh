# -*- coding: utf-8 -*-

from cStringIO import StringIO
from pylons import config
import Image
import logging
import os
import random
import string

log = logging.getLogger(__name__)
class Photo(object):
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content
        
    def relative_path(self, filename):
        """return the file path relative to root
        """
        rdir = lambda: ''.join(random.sample(string.ascii_lowercase, 8))
        path = '/'.join([rdir(), filename])
        return path
    
    def thumbnail_url(self, thumbnail_size):
        url = self.relative_path(
            self.filename.replace(os.sep, '_')
        ) 
        path = os.path.join(
            config['app_conf']['permanent_store'],
            url
        )
        dirname = os.path.dirname(path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        avatar = Image.open(StringIO(self.content))
        avatar.thumbnail(thumbnail_size)
        avatar.save(path)
        return url
