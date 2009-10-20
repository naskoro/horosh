# -*- coding: utf-8 -*-

from formencode.validators import *
from cgi import FieldStorage
from cStringIO import StringIO
import logging
import Image

log = logging.getLogger(__name__)

class FileUploadValidator(FancyValidator):
    pass

class ImageUploadValidator(FileUploadValidator):
    messages = {
        'invalid_image': u'Ваш файл не каринка или испорченая картика'
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
