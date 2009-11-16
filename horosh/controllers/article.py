# -*- coding: utf-8 -*-

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import HasAuthKitRole
from datetime import datetime
from horosh import form, model
from horosh.lib.base import BaseController, render, redirect_to, is_ajax, \
    current_user, is_admin
from horosh.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort
from pytils import translit
from routes import url_for
from sqlalchemy.orm.exc import NoResultFound
import logging
import time

log = logging.getLogger(__name__)

class ArticleForm(form.FieldSet):
    def __init__(self, name, path=None):
        self.path_ecxept = path
        super(ArticleForm, self).__init__(name)
        
    def init(self):
        self.adds(
            form.Field('title', validator=form.v.String(not_empty=True)),
            form.Field('path', validator=form.v.All(
                form.v.Slug(), 
                form.v.UniqueModelField(
                    model=model.Article, 
                    field=model.Article.path,
                    except_=self.path_ecxept
                )
            )),
            form.Field('content', validator=form.v.String(not_empty=True)),
            form.Field('save'),
            form.Field('save_view'),
            form.Field('cancel')
        )
    
class ArticleController(BaseController):
    @authorize(HasAuthKitRole('admin'))
    def new(self, label=None):
        
        fs = ArticleForm('article-new')

        if request.POST and fs.fields.cancel.id in request.POST:
            if label is not None:
                return redirect_to(label)
            return redirect_to('article_list')

        if request.POST and fs.is_valid(request.POST):
            node = model.Article()
            node.title = fs.fields.title.value
            node.content = fs.fields.content.value
            node.label = label
            node.node_user_id = current_user().id

            is_valid = True
            if not fs.fields.path.value:
                fs.fields.path.value = translit.slugify(node.title)
                is_valid = fs.is_valid(fs.get_values(use_ids=True))
            
            if is_valid:
                node.path = fs.fields.path.value
                
                meta.Session.add(node)
                meta.Session.commit()
                
                if fs.fields.save_view.id in request.POST:
                    return redirect_to(node.url())
                else:
                    if node.label is not None:
                        return redirect_to(node.label)
                    return redirect_to('article_list')
            
        c.form = fs
        c.fs = fs.fields
        
        if is_ajax():
            result = render('/article/new_partial.html')
        else:
            result = render('/article/new.html')
        if request.POST:
            result = fs.htmlfill(result)
        return result

    def show(self, id=None, path=None):
        node = None

        if id is None or path is None:
            if id is not None:
                node = self._get_row(model.Article, id)
            if path is not None:
                try:
                    node = meta.Session.query(model.Article)\
                           .filter_by(path=path).one()
                except NoResultFound:
                    abort(404)
                    
        if node is None:
            abort(404)
            
        if not is_admin() and node.published is None:
            abort(403) 
        
        c.node = node
        return render('/article/show.html')
    
    def list(self, label=None):
        query = meta.Session().query(model.Article)
        
        if label is not None:
            query = query.filter(model.Article.label==label)
        else:
            query = query.filter(model.Article.label==label)
        
        if not is_admin():
            query = query.filter(model.Article.published != None)
                
        query = query.order_by(model.Article.created.desc())
        
        c.nodes = query.all()
        c.label = label
        return render('/article/list.html')
    
    @authorize(HasAuthKitRole('admin'))
    def edit(self, id):
        node = self._get_row(model.Article, id)

        fs = ArticleForm('article-edit', node.path)
         
        if request.POST and fs.fields.cancel.id in request.POST:
            if self.back_page():
                return redirect_to(**self.back_page())
            return redirect_to(node.url())

        if request.POST and fs.is_valid(request.POST):
            
            node.title = fs.fields.title.value
            node.content = fs.fields.content.value
            
            is_valid = True
            if not fs.fields.path.value:
                fs.fields.path.value = translit.slugify(node.title)
                is_valid = fs.is_valid(fs.get_values(use_ids=True))
            
            if is_valid:
                node.path = fs.fields.path.value
                
                meta.Session.commit()
                if fs.fields.save_view.id in request.POST:
                    return redirect_to(node.url())
                else:
                    if node.label is not None:
                        return redirect_to(node.label)
                    return redirect_to('article_list')

        if not request.POST:
            fs.set_values({
                'title': node.title,
                'path': node.path,
                'content': node.content
            })
        
        c.form = fs
        c.fs = fs.fields
        c.node = node
        
        if is_ajax():
            result = render('/article/edit_partial.html')
        else:
            result = render('/article/edit.html')
        return fs.htmlfill(result)
    
    @authorize(HasAuthKitRole('admin'))
    def publish(self, id, published):
        node = self._get_row(model.Article, id)

        if published=='1':
            node.published = datetime.now()
        else:
            node.published = None 
            
        meta.Session.commit()
        if self.back_page():
            return redirect_to(**self.back_page())
        return redirect_to(node.url())

    @authorize(HasAuthKitRole('admin'))
    def remove(self, id):
        node = self._get_row(model.Article, id)
        
        meta.Session.delete(node)
        meta.Session.commit()
        if self.back_page() is not None:
            return redirect_to(self.back_page())
        return redirect_to('article_list')