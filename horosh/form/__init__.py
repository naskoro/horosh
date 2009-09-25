# -*- coding: utf-8 -*-

from formalchemy import validators
from formalchemy import forms
from formalchemy import tables
from sqlalchemy import types

from horosh.form import config
from horosh.form import fields
         
class FieldSet(forms.FieldSet):
    default_renderers = {
        types.String: fields.TextFieldRenderer,
        types.Integer: fields.IntegerFieldRenderer,
        types.Boolean: fields.CheckBoxFieldRenderer,
        types.DateTime: fields.DateTimeFieldRenderer,
        types.Date: fields.DateFieldRenderer,
        types.Time: fields.TimeFieldRenderer,
        types.Binary: fields.FileFieldRenderer,
        'dropdown': fields.SelectFieldRenderer,
        'checkbox': fields.CheckBoxSet,
        'radio': fields.RadioSet,
        'password': fields.PasswordFieldRenderer,
        'textarea': fields.TextAreaFieldRenderer,
    }


class Grid(tables.Grid):
    pass