from docutils.core import publish_parts
from horosh.model import meta
from horosh import model

def rest2html(text):
    text = publish_parts(
        text, 
        writer_name='html',
        settings_overrides=dict(file_insertion_enabled=False, raw_enabled=False)
    )
    return text['html_body']

def getCurrentUser():
    user = meta.Session.query(model.User).filter_by(email='naspeh@pusto.org').one()
    return user 