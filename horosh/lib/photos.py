# -*- coding: utf-8 -*-

from cStringIO import StringIO
from gdata.photos import service
from horosh.lib.base import render
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

class Picasa(object):
    client = service.PhotosService()
    _count = 0
    
    def photos(self, user, albumid, limit=None):
        url = 'http://picasaweb.google.com/data/feed/api/user/%s/albumid/%s?kind=photo' % (user, albumid)
        return self.client.GetFeed(url, limit=limit)

    def render(self, photos, photos_list=[], limit=None, 
               align=None, count_per_page=5, template='/util/gallery.html'):
        photos = photos.entry
        result = []
        if photos_list:
            for photo in photos:
                if photo.gphoto_id.text in photos_list :
                    result.append(self.photo_prepare(photo))
        else:
            for photo in photos:
                result.append(self.photo_prepare(photo))
        Picasa._count += 1
        return render(template, {
            'id': 'gallery-' + str(self._count),
            'align': align,
            'photos': result,
            'count_per_page': count_per_page
        })

    def photo_url(self, photo):
        return photo.media.content[0].url
    
    def photo_prepare(self, photo):
        result = dict(
            url = self.photo_url(photo),
            url_pattern = self.photo_url(photo) + '?imgmax=%s', 
            name = photo.title.text,
            title = photo.summary.text or photo.title.text 
        )
        return result

def picasa_by_user(username, albumid, limit, **kwargs):
    picasa = Picasa()
    data = picasa.photos(username, albumid, limit)
    return picasa.render(data, **kwargs)

def picasa_by_data(data, **kwargs):
    picasa = Picasa()
    return picasa.render(data, **kwargs)