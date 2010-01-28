# -*- coding: utf-8 -*-

from formencode import Schema, htmlfill, Invalid, variabledecode
from horosh.lib.base import render
from pylons import request
import logging

log = logging.getLogger(__name__)

class FieldSet(object):

    class Fields(object):
        def __init__(self, fields={}):
            self._fields = fields
        def __getattr__(self, name):
            if name in self._fields:
                return self._fields[name]
            return None
        def __iter__(self):
            return self
        def next(self):
            return self._fields.next()
        def add(self, field):
            self._fields[field.name] = field
        def values(self):
            return self._fields.values()
        def items(self):
            return self._fields.items()

    def __init__(self, name):
        self.action = request.path_qs
        schema = Schema()
        schema.allow_extra_fields = True
        schema.filter_extra_fields = True
        self.schema = schema
        self.name = name
        self.errors = None
        self.fields = self.Fields()
        self.init()

    def init(self):
        pass

    def add(self, field):
        field.id = self.get_field_id(field.name)
        self.fields.add(field)
        if field.validator is not None:
            self.schema.add_field(field.name, field.validator)
        return self

    def adds(self, *fields):
        for field in fields:
            self.add(field)

    def add_pre_validator(self, validator):
        self.schema.add_pre_validator(validator)
        return self

    def get_field_id(self, name):
        if self.name:
            return self.name + '-' + name
        return name

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

    def clean(self):
        for field in self.fields.values():
            field.value = None
        return self

    def _render(self, template, template_partial, with_htmlfill=True):
        if request.is_xhr or 'is_ajax' in request.params:
            template = template_partial
        if with_htmlfill or self.errors:
            result = self.htmlfill(render(template))
        else:
            result = render(template)
        return result

    def htmlfill(self, form):
        return htmlfill.render(form, self.get_values(use_ids=True), errors=self.errors)

    def is_valid(self, params):
        self.set_values(params, use_ids=True)
        params = self.get_values()
        result = True
        try:
            params = variabledecode.variable_decode(params, '.', '--')
            form_result = self.schema.to_python(params)
            self.set_values(form_result)
        except Invalid, e:
            self.set_errors(e.unpack_errors())
            result = False

        return result

    def set_errors(self, errors):
        if isinstance(errors, (str, unicode)):
            self.errors = errors
            return
        result = {}
        for key, error in errors.items():
            if key == 'form':
                result[key] = error
            else:
                result[self.get_field_id(key)] = error
        self.errors = result

    def has_errors(self, name='form'):
        if self.errors is None:
            return False
        try:
            self.errors[name]
        except KeyError:
            return False
        return True

class Field(object):
    def __init__(self, name=None, id=None, validator=None, label=None,
                 instructions=None, value = None):
        self.name = name
        self.validator = validator
        self.label = label
        self.instructions = instructions
        self.id = id
        self.value = value

    def not_empty(self):
        if self.validator is not None and hasattr(self.validator, 'not_empty'):
            return self.validator.not_empty
        return False
