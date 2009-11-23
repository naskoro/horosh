# -*- coding: utf-8 -*-

from docutils import nodes
from docutils.core import publish_parts
from docutils.parsers.rst import directives, Directive
from html5lib import treebuilders
from mako.template import Template
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.special import TextLexer
from pylons.templating import pylons_globals
from webhelpers.text import truncate
import html5lib
import logging

log = logging.getLogger(__name__)

# Set to True if you want inline CSS styles instead of classes
INLINE_STYLES = False

# The default formatter
DEFAULT = HtmlFormatter(noclasses=INLINE_STYLES)

# Add name -> formatter pairs for every variant you want to use
VARIANTS = {
    'linenos': HtmlFormatter(noclasses=INLINE_STYLES, linenos=True),
}

class Pygments(Directive):
    """ Source code syntax hightlighting.
    """
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = dict([(key, directives.flag) for key in VARIANTS])
    has_content = True

    def run(self):
        self.assert_has_content()
        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = TextLexer()
        # take an arbitrary option if more than one is given
        formatter = self.options and VARIANTS[self.options.keys()[0]] or DEFAULT
        parsed = highlight(u'\n'.join(self.content), lexer, formatter)
        return [nodes.raw('', parsed, format='html')]

directives.register_directive('code-block', Pygments)

def rst2html(text, use_ext=True):
    text = publish_parts(
        text,
        writer_name='html',
        settings_overrides=dict(file_insertion_enabled=False, raw_enabled=False)
    )
    result = text['html_body']
    if use_ext:
        globs = pylons_globals()
        template = Template(result)
        result = template.render_unicode(**globs)

    return result

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
