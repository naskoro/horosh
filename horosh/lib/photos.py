# -*- coding: utf-8 -*-

import logging
from gdata.photos import service
from webhelpers.html import tags

log = logging.getLogger(__name__)

class Picasa(object):
    client = service.PhotosService()
    
    @staticmethod
    def debug(debug=True):
        Picasa.client.debug = debug
    
    @staticmethod
    def photos(username, albumid, limit=None):
        photos = Picasa.client.GetFeed(
            '/data/feed/api/user/%s/albumid/%s?kind=photo' % (username, albumid), 
            limit=limit
        ).entry
        return photos
    
    @staticmethod
    def photo_url(photo):
        return photo.media.content[0].url
    
    @staticmethod
    def render(username, albumid, *photos_list):
        photos = Picasa.photos(username, albumid)
        result = photos
        if photos_list:
            result = []
            for photo in photos:
                if photo.gphoto_id.text in photos_list:
                    result.append(photo)
        photos = []
        for item in result:
            url = Picasa.photo_url(item)
            el = tags.image(url + '?imgmax=288', item.title.text)
            el = tags.link_to(el, url + '?imgmax=640')
            photos.append(el)
        return tags.ul(photos)