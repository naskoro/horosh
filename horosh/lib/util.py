# -*- coding: utf-8 -*-

from Image import ANTIALIAS
from cStringIO import StringIO
from docutils.core import publish_parts
from html5lib import treebuilders
from webhelpers.text import truncate
from horosh.lib import rst
import Image
import html5lib
import logging

log = logging.getLogger(__name__)

SHORT_HTML_SEPARATOR = '<hr class="docutils" />'

def rst2html(text):
    rst.add_pygments()
    text = publish_parts(
        text,
        writer_name='html',
        settings_overrides=dict(file_insertion_enabled=False, raw_enabled=False)
    )
    return text['html_body']

def shortable_html(html):
    return SHORT_HTML_SEPARATOR in html

def clean_html(html):
    return html.replace(SHORT_HTML_SEPARATOR, '')

def short_html(html):
    document = html.split(SHORT_HTML_SEPARATOR, 1)[0]

    parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))
    document = parser.parse(document)

    xml = document.getElementsByTagName('body')[0].childNodes[0].toxml()
    return xml

def truncate_html(*args):
    document = truncate(*args)
    parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))
    document = parser.parse(document)

    xml = document.getElementsByTagName('body')[0].childNodes[0].toxml()
    return xml

def human_filesize(size):
    for x in ['bytes','KB','MB','GB','TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0

def avatar_prepare(avatar, size=(100,100)):
    pic = Image.open(avatar)
    pic.thumbnail(size, ANTIALIAS)
    buffer = StringIO()
    pic.save(buffer, pic.format, quality=100)
    buffer.seek(0)
    return buffer.read()
