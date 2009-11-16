# -*- coding: utf-8 -*-
from horosh.lib.base import current_user, render

def sidebar():
    params = dict(
        user=current_user()
    )
    return render('/sidebar.html', params)
