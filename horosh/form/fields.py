# -*- coding: utf-8 -*-

from formencode import Schema, htmlfill
from pylons.decorators import validate
from pylons import request

from horosh.lib.base import render
class FieldSet(object):
    def __init__(self, name, *fields):
        schema = Schema()
        schema.allow_extra_fields = True
        schema.filter_extra_fields = True
        self._schema = schema
        self._name = name
        self._fields = {}
        if fields:
            for field in fields:
                self.add(field)
        self.init()
    def init(self):
        pass
    def __getattr__(self, name):
        if name in self._fields:
            return self._fields[name]
    def add(self, field):
        field.id = self._get_id(field.name) 
        self._fields[field.name] = field
        self._schema.add_field(field.id, field.validator)
        return self
    def add_pre_validator(self, validator):
        self._schema.add_pre_validator(validator)
        return self
    def _get_id(self, name):
        return self._name + '.' + name
    def get_values(self, use_ids=False):
        values = {}
        if use_ids:
            values = {}
            for field in self._fields.values():
                values[field.id] = field.value
            return values

        for name, field in self._fields.items():
            values[name] = field.value
        return values
    def set_values(self, params, use_ids=False):
        if use_ids:
            for name, field in self._fields.items():
                if(field.id in params):
                    field.value = params[field.id]
            return
        
        for name, field in self._fields.items():
            if(name in params):
                field.value = params[name]
    def clean(self):
        for field in self._fields.values():
            field.value = None
        return self
    def render(self, template, template_partial, with_htmlfill=True):
        if request.is_xhr:
            template = template_partial
        if with_htmlfill:
            result = self.htmlfill(render(template))
        else:
            result = render(template)
        return result
    def htmlfill(self, form):
        return htmlfill.render(form, self.get_values(use_ids=True))
    def validate(self, **kwargs):
        return validate(self._schema, **kwargs)

class Field(object):
    def __init__(self, name=None, id=None, validator=None, label=None, 
                 instructions=None, value = None):
        self.name = name
        self.validator = validator
        self.label = label
        self.instructions = instructions
        self.id = id
        self.value = value