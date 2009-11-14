# -*- coding: utf-8 -*-

from cStringIO import StringIO
from formencode.validators import *
from horosh.lib import picasa
import Image
import logging

log = logging.getLogger(__name__)

class FileUploadValidator(FancyValidator):
    pass

class ImageUploadValidator(FileUploadValidator):
    messages = {
        'invalid_image': u'Ваш файл не картинка или испорченая картинка'
    }
    def validate_python(self, value, state):
        file = StringIO(value.value)
        try:
            # load() is the only method that can spot a truncated JPEG,
            #  but it cannot be called sanely after verify()
            trial_image = Image.open(file)
            trial_image.load()
            
            # Since we're about to use the file again we have to reset the
            # file object if possible.
            if hasattr(file, 'reset'):
                file.reset()
                
            # verify() is the only method that can spot a corrupt PNG,
            #  but it must be called immediately after the constructor
            trial_image = Image.open(file)
            trial_image.verify()
        except Exception: # Python Imaging Library doesn't recognize it as an image
            raise Invalid(self.message('invalid_image', state), value, state)

class PicasaUserValidator(FancyValidator):
        
    messages = {
        'invalid_user': u'Неправильное имя'
    }
    
    def validate_python(self, value, state):
        value = value.strip()
        if not picasa.user_validate(value):
            error_message = self.message('invalid_user', state)
            raise Invalid(error_message, value, state)
            
class PicasaAlbumValidator(FormValidator):
    show_match = False
    field_names = None
    validate_partial_form = True
    __unpackargs__ = ('*', 'field_names')
        
    messages = {
        'invalid_albumid': u'Неправильный ID'
    }
    
    def __init__(self, *args, **kw):
        super(FormValidator, self).__init__(*args, **kw)
        if len(self.field_names) < 2:
            raise TypeError("FieldsMatch() requires at least two field names") 
   
    def validate_python(self, field_dict, state):
        user = field_dict[self.field_names[0]]
        albumid = field_dict[self.field_names[1]]
        if not picasa.album_validate(user, albumid):
            error_message = self.message('invalid_albumid', state)
            errors = {
                self.field_names[1]: Invalid(error_message, field_dict, state)
            }
            raise Invalid(error_message, field_dict, state, error_dict= errors)