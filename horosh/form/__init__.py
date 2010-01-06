# -*- coding: utf-8 -*-

from horosh.form import validators as v
from horosh.form.fields import FieldSet, Field

class DeleteAcceptForm(FieldSet):
    def init(self):
        self.adds(
            Field('save'),
            Field('cancel')
        )
