# -*- coding: utf-8 -*-

import logging
import re

log = logging.getLogger(__name__)

PATTERN = r'(?si)<script type=\"text\/javascript\">(.+?)<\/script>'

def clean(xhtml):
    return re.sub(PATTERN, '', xhtml)

def scripts(xhtml):
    res = re.findall(PATTERN, xhtml)
    res = ''.join(res)
    res = re.sub(r'(?si)\/\*.+?\*\/', '', res)
    return res