from gdata.photos import service

class Picasa(object):
    client = service.PhotosService()
    
    @staticmethod
    def setDebug(debug=True):
        Picasa.client.debug = debug
    
    @staticmethod
    def getPhotos(username, albumid):
        photos = Picasa.client.GetFeed(
            '/data/feed/api/user/%s/albumid/%s?kind=photo' % (username, albumid), 
            limit=10
        ).entry
        return photos
    
    @staticmethod
    def getPhotoUrl(photo):
        return photo.media.content[0].url