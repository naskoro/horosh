# -*- coding: utf-8 -*-

from horosh.lib.base import render

def field(field, **kwargs):
    return render('forms/field.html', {'field': field, 'kwargs': kwargs})