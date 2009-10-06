# -*- coding: utf-8 -*-

import logging
from gdata.photos import service
from webhelpers.html import tags
from horosh.lib.base import render

log = logging.getLogger(__name__)

class Picasa(object):
    client = service.PhotosService()
    _count = 0
    
    @staticmethod
    def debug(debug=True):
        Picasa.client.debug = debug
    
    @staticmethod
    def photos(user, album, limit=None):
        url = '/data/feed/api/user/%s/albumid/%s?kind=photo' % (user, album)
        return Picasa.client.GetFeed(url, limit=limit).entry

    @staticmethod
    def photo_url(photo):
        return photo.media.content[0].url
    
    @staticmethod
    def render(username, albumid, photos_list=[], limit=None, 
               align=None, count_per_page=5, template='/util/gallery.html'):
        photos = Picasa.photos(username, albumid, limit)
        result = []
        if photos_list:
            for photo in photos:
                if photo.gphoto_id.text in photos_list :
                    result.append(Picasa.photo_prepare(photo))
        else:
            for photo in photos:
                result.append(Picasa.photo_prepare(photo))
        if align:
            count_per_page = 1
        pages = []
        count_pages = len(result) / count_per_page
        if count_pages * count_per_page != len(result):
            count_pages += 1
        for page in xrange(count_pages):
            index = page*count_per_page
            pages.append(result[index : index+count_per_page])
        
        Picasa._count += 1
        return render(template, {
            'id': 'gallery-' + str(Picasa._count),
            'align': align,
            'pages': pages,
            'pages_count': len(pages)
        })
    
    @staticmethod
    def photo_prepare(photo):
        result = dict(
            url = Picasa.photo_url(photo),
            url_pattern = Picasa.photo_url(photo) + '?imgmax=%s', 
            name = photo.title.text,
            title = photo.summary.text or photo.title.text 
        )
        log.debug(result)
        return result