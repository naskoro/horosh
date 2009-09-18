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
        #client.ClientLogin('naspeh', 'Pu100...')
        client.debug = True
        self.client = client
        
    def galleryview(self):
        photos = []
        for item in self.getPhotos('naspeh', '20090306_Krym_Noviy_svet'):
            photos.append(tags.image(self.getPhotoUrl(item) + '?imgmax=200', item.title.text, title=item.title.text))
        c.photos = photos 
        return render('/test/galleryview.html')
    
    def popeye(self):
        photos = []
        for item in self.getPhotos('naspeh', '20090306_Krym_Noviy_svet'):
            url = self.getPhotoUrl(item)
            el = tags.image(url + '?imgmax=288', item.title.text, title=item.title.text)
            el = tags.link_to(el, url + '?imgmax=640')
            photos.append(el)
        c.photos = photos 
        return render('/test/popeye.html')
    
    def getPhotos(self, userName, albumName):
        album = self.getAlbum(userName, albumName) 
        photos = self.client.GetFeed(album.GetPhotosUri(), limit=10).entry
        return photos
    
    def getPhotoUrl(self, photo):
        return photo.media.content[0].url
    
    def getAlbum(self, userName, albumName):
        # Get all albums
        albums = self.client.GetUserFeed(user=userName)
        for item in albums.entry:
            if (item.name.text == albumName):
                return item
        return None