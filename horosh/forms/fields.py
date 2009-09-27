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
        self.schema = schema
        self.name = name
        self.fields = {}
        if fields:
            for field in fields:
                self.add(field)
    def add(self, field):
        field.id = self._get_id(field.name) 
        self.fields[field.name] = field
        self.schema.add_field(field.id, field.validator)
        return self
    def add_pre_validator(self, validator):
        self.schema.add_pre_validator(validator)
        return self
    def _get_id(self, name):
        return self.name + '_' + name
    def get_values(self, use_ids=False):
        values = {}
        if use_ids:
            values = {}
            for field in self.fields.values():
                values[field.id] = field.value
            return values

        for name, field in self.fields.items():
            values[name] = field.value
        return values
    def set_values(self, params, use_ids=False):
        if use_ids:
            for name, field in self.fields.items():
                if(field.id in params):
                    field.value = params[field.id]
            return
        
        for name, field in self.fields.items():
            if(name in params):
                field.value = params[name]
    def get_value(self, name):
        if name in self.fields:
            return self.fields[name].value
        return None
    def set_value(self, name, value):
        if name in self.fields:
            self.fields[name].value = value
    def render(self, template):
        return htmlfill.render(render(template), self.get_values(use_ids=True))
    def validate(self, **kwargs):
        return validate(self.schema, **kwargs)

class Field(object):
    def __init__(self, name, validator=None, label=None, instructions=None):
        self.name = name
        self.validator = validator
        self.label = label
        self.instructions = instructions
        self.id = None
        self.value = None