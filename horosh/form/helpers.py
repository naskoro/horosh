# -*- coding: utf-8 -*-

from formalchemy import base

from horosh.lib.base import render

def field(field, field_type='long'):
    return render('forms/field.html', {'field': field, 'field_type': field_type})

def prettify(text):
    return base.prettify(text)