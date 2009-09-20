import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from webhelpers.html import tags

from horosh.lib.base import BaseController, render

log = logging.getLogger(__name__)

class DummyController(BaseController):

    def __init__(self):
        from gdata.photos import service
        client =service.PhotosService()
        #client.debug = True
        self.client = client
        
    def galleryview(self):
        photos = []
        for item in self.getPhotos('naspeh', '5322049975408703009'):
            photos.append(tags.image(
                self.getPhotoUrl(item) + '?imgmax=200', 
                item.title.text, 
                title=item.title.text
            ))
        c.photos = photos 
        return render('/dummy/galleryview.html')
    
    def popeye(self):
        photos = []
        for item in self.getPhotos('naspeh', '5322049975408703009'):
            url = self.getPhotoUrl(item)
            el = tags.image(url + '?imgmax=288', item.title.text, title=item.title.text)
            el = tags.link_to(el, url + '?imgmax=640')
            photos.append(el)
        c.photos = photos 
        return render('/dummy/popeye.html')
    
    def getPhotos(self, username, albumid):
        photos = self.client.GetFeed(
            '/data/feed/api/user/%s/albumid/%s?kind=photo' % (username, albumid), 
            limit=10
        ).entry
        return photos
    
    def getPhotoUrl(self, photo):
        return photo.media.content[0].url