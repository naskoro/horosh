# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import HasAuthKitRole
from pylons import request, tmpl_context as c
from pylons.controllers.util import abort
from pytils import translit
from sqlalchemy.orm.exc import NoResultFound

from horosh import form, model
from horosh.lib.base import BaseController, render, redirect_to, flash, \
                            is_ajax, current_user, is_admin, pager_or_404
from horosh.model import meta


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
            form.Field('save_view_list'),
            form.Field('cancel')
        )


class ArticleController(BaseController):
    @authorize(HasAuthKitRole('admin'))
    def new(self, label=None):

        fs = ArticleForm('article-new')

        if request.POST and fs.fields.cancel.id in request.POST:
            if label is not None:
                return redirect_to(label)
            return redirect_to('articles')

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
                elif fs.fields.save_view_list.id in request.POST:
                    if node.label is not None:
                        return redirect_to(node.label)
                    return redirect_to('articles')
                else:
                    return redirect_to(node.url_edit())

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
        self.is_page_back = True
        query = meta.Session().query(model.Article)

        if label is not None:
            query = query.filter(model.Article.label==label)
        else:
            query = query.filter(model.Article.label==label)

        if not is_admin():
            query = query.filter(model.Article.published != None)

        query = query.order_by(model.Article.created.desc())

        c.nodes = pager_or_404(query)
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
                flash(u'Статья успешно сохранена')
                if fs.fields.save_view.id in request.POST:
                    return redirect_to(node.url())
                elif fs.fields.save_view_list.id in request.POST:
                    if node.label is not None:
                        return redirect_to(node.label)
                    return redirect_to('articles')

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
            message = u'Статья успешно опубликована'
        else:
            node.published = None
            message = u'Статья успешно сохранена как черновик'

        meta.Session.commit()
        flash(message)
        if self.back_page():
            return redirect_to(**self.back_page())
        return redirect_to(node.url())

    @authorize(HasAuthKitRole('admin'))
    def remove(self, id):
        node = self._get_row(model.Article, id)

        fs = form.DeleteAcceptForm('article-remove')

        if request.POST:
            if fs.fields.save.id in request.POST:
                meta.Session.delete(node)
                meta.Session.commit()
                flash(u'Статья успешно удалена')
            if self.back_page() is not None:
                return redirect_to(**self.back_page())
            return redirect_to('articles')
        else:
            c.form = fs
            if is_ajax():
                result = render('/util/delete_accept_partial.html')
            else:
                result = render('/util/delete_accept.html')
            return result
