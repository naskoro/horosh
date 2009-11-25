# -*- coding: utf-8 -*-

from gdata.photos import service
from horosh.lib.base import render as render_
from urllib import urlopen
from gdata.photos.service import GooglePhotosException
import gdata
import logging

log = logging.getLogger(__name__)

client = service.PhotosService()

URL_ALBUM = 'http://picasaweb.google.com/data/feed/api/user/%s/album/%s?kind=photo'
URL_USER = 'http://picasaweb.google.com/data/feed/api/user/%s/?kind=album'

def photos(user, albumid, limit=None):
    url = URL_ALBUM % (user, albumid)
    return urlopen(url).read()

class _render:
    def __init__(self):
        self.count=0
    def __call__(self, photos, photos_list=[], limit=30,
           align=None, count_per_page=5, template='/util/gallery.html'):

        def photo_url(photo):
            return photo.content.src

        def photo_prepare(photo):
            result = dict(
                url = photo_url(photo),
                url_pattern = photo_url(photo) + '?imgmax=%s',
                name = photo.title.text,
                title = photo.summary.text or photo.title.text
            )
            return result

        photos = gdata.GDataFeedFromString(photos)
        photos = photos.entry[0:limit]
        result = []
        if photos_list:
            for photo in photos:
                if photo.gphoto_id.text in photos_list :
                    result.append(photo_prepare(photo))
        else:
            for photo in photos:
                group = photo.FindExtensions('group')
                keywords = group[0].FindChildren('keywords')[0].text
                
                if keywords:
                    keywords = keywords.split(', ')
                else:
                    keywords = ()
                    
                if u'hide' not in keywords:
                    result.append(photo_prepare(photo))
                
        self.count = self.count+1
        return render_(template, {
            'id': 'gallery-' + str(self.count),
            'align': align,
            'photos': result,
            'count_per_page': count_per_page
        })

render = _render()

def album_validate(user, albumid):
    url = URL_ALBUM % (user, albumid)
    try:
        client.GetFeed(url, limit=1)
    except GooglePhotosException:
        return False
    return True

def user_validate(user):
    url = URL_USER % user
    try:
        client.GetFeed(url, limit=1)
    except GooglePhotosException:
        return False
    return True

def render_by_user(username, albumid, limit, **kwargs):
    data = photos(username, albumid, limit)
    return render(data, **kwargs)
