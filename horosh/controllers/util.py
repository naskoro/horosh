# -*- coding: utf-8 -*-

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser, HasAuthKitRole
from cStringIO import StringIO
from datetime import datetime
from horosh import model
from horosh.lib import picasa
from horosh.lib.base import BaseController, render
from horosh.lib.util import rst2html
from horosh.model import meta
from mimetypes import guess_type
from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators.rest import restrict
from webhelpers.markdown import markdown
import Image
import codecs
import logging
import os
import yaml

log = logging.getLogger(__name__)

THUMBNAIL_SIZE = 100, 100

class UtilController(BaseController):
    @authorize(ValidAuthKitUser())
    def login(self):
        c.message = u'Login success'
        return redirect_to('/')
    
    @authorize(ValidAuthKitUser())
    def logout(self):
        c.message = u'Logout success'
        return redirect_to('/')
    
    @authorize(HasAuthKitRole('admin'))
    def demo_up(self):
        event = meta.Session.query(model.Event).filter(
            model.Event.id == 1
        ).one()
        
        user = meta.Session.query(model.User).filter(
            model.User.nickname == 'nobody'
        ).one()
        
        for node in event.persons: meta.Session.delete(node)
        for node in event.reports: meta.Session.delete(node)
        for node in event.albums: meta.Session.delete(node)
        
        meta.Session.commit()
        
        dir = config['demo_dir']

        info_file = os.path.join(dir, 'info.yml')
        info = codecs.open(info_file, 'r', 'utf-8')
        info = yaml.load(info)

        event.title = info['title']
        event.node_user = user
        event.created = datetime.now()
        
        if 'albums' in info:
            for album in info['albums']:
                node = model.Album()
                node.settings = picasa.photos(album['user'], album['albumid'], 15)
                node.node_user = user
                node.events = [event]
                meta.Session.add(node)
        
        
        persons_dir = os.path.join(dir, 'persons')
        for file in os.listdir(persons_dir):
            path =  os.path.join(persons_dir, file)
            if os.path.isfile(path):
                node = model.Person()
                node.fullname = file.split('.')[0]
                node.avatar = self._avatar_prepare(open(path, 'r'))
                node.node_user = user
                node.event = event
                meta.Session.add(node)
                
        reports_dir = os.path.join(dir, 'reports')            
        for file in os.listdir(reports_dir):
            path =  os.path.join(reports_dir, file)
            if os.path.isfile(path):
                text = codecs.open(path, 'r', 'utf-8').read()
                node = model.Report()
                node.content = text                    
                node.node_user = user
                node.event = event
                meta.Session.add(node)
        
        meta.Session.commit()
        
        c.message = u'Демонстрация обновлена'
        c.type = 'success'
        return render('/util/message.html')
    
    @restrict('POST')
    def markdown(self):
        text = request.POST['data'] 
        if text is None:
            abort(400)
        c.content = markdown(text)     
        return render('/util/response.html')

    @restrict('POST')
    def rst(self):
        text = request.POST['data'] 
        if c.content is None:
            abort(400)
        text = rst2html(text)
        c.content = text     
        return render('/util/response.html')
    
    def flash_file(self, id):
        if id in session['flash_file']:
            file =  session['flash_file'][id];
        else:
            abort(404)
        data = file['content']
        response.content_type = guess_type(file['filename'])[0] or 'text/plain'
        return data

    def _avatar_prepare(self, avatar):
        pic = Image.open(avatar)
        pic.thumbnail(THUMBNAIL_SIZE)
        buffer = StringIO()
        pic.save(buffer, pic.format)
        buffer.seek(0)
        return buffer.read()
