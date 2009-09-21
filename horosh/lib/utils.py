from docutils.core import publish_parts

def rest2html(text):
    text = publish_parts(
        text, 
        writer_name='html',
        settings_overrides=dict(file_insertion_enabled=False, raw_enabled=False)
    )
    return text['html_body'] 