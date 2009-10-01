import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from webhelpers.html import tags

from horosh.lib.base import BaseController, render
from horosh.lib.photos import Picasa 

log = logging.getLogger(__name__)

class DummyController(BaseController):

    def popeye(self):
        #Picasa.debug()
        photos = []
        for item in Picasa.photos('naspeh', '5322049975408703009', limit=5):
            url = Picasa.photo_url(item)
            el = tags.image(url + '?imgmax=288', item.title.text)
            el = tags.link_to(el, url + '?imgmax=640')
            photos.append(el)
        c.photos = photos 
        return photos