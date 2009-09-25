# -*- coding: utf-8 -*-

import logging
from formalchemy.fields import FieldRenderer, EscapingReadonlyRenderer,    \
                               TextFieldRenderer, IntegerFieldRenderer,    \
                               FloatFieldRenderer, PasswordFieldRenderer,  \
                               TextAreaFieldRenderer, HiddenFieldRenderer, \
                               CheckBoxFieldRenderer, FileFieldRenderer,   \
                               RadioSet, CheckBoxSet, SelectFieldRenderer, \
                               AbstractField, Field, AttributeField
from formalchemy import helpers as h
from formalchemy.ext.fsblob import FileFieldRenderer
from formalchemy.ext.fsblob import ImageFieldRenderer
from webhelpers.html import tags

log = logging.getLogger(__name__)

class DateFieldRenderer(FieldRenderer):
    
    """render a date as a text field"""
    format = '%Y-%m-%d'
    def render(self, **kwargs):
        return h.text_field(self.name, value=self._value, maxlength=10, **kwargs)

class TimeFieldRenderer(FieldRenderer):
    """render a time as a text field"""
    format = '%H:%M'
    def render(self, **kwargs):
        return h.text_field(self.name, value=self._value, maxlength=5, **kwargs)
    
class DateTimeFieldRenderer(FieldRenderer):
    """render a date time as a text field"""
    format = '%Y-%m-%d %H:%M:%S'
    def render(self, **kwargs):
        return h.text_field(self.name, value=self._value, maxlength=16, **kwargs)