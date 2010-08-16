# -*- coding: utf-8 -*-

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser
from datetime import datetime
from horosh import form, model
from horosh.lib.base import BaseController, render, redirect_to, flash, is_ajax, \
    current_user
from horosh.model import meta
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort
from sqlalchemy import and_
from sqlalchemy.orm import join
from sqlalchemy.orm.exc import NoResultFound
from webhelpers import paginate
import logging

log = logging.getLogger(__name__)

DATE_FORMAT = '%d/%m/%Y'
MONTH_STYLE = 'dd/mm/yyyy' # 'dd/mm/yyyy' or 'mm/dd/yyyy'

class EventForm(form.FieldSet):
    def init(self):
        self.adds(
            form.Field('title', validator=form.v.String(not_empty=True, max=50)),
            form.Field('start',
                validator=form.v.DateConverter(
                    not_empty=True,
                    month_style=MONTH_STYLE
                )
            ),
            form.Field('finish',
                validator=form.v.DateConverter(
                    not_empty=True,
                    month_style=MONTH_STYLE
                )
            ),
            form.Field('summary', validator=form.v.String(max=1000)),
            form.Field('save'),
            form.Field('cancel')
        )

class EventController(BaseController):
    @authorize(ValidAuthKitUser())
    def new(self):
        fs = EventForm('event-new')

        if request.POST and fs.fields.cancel.id in request.POST:
            return redirect_to(current_user().url())

        if request.POST and fs.is_valid(request.POST):
            node = model.Event()
            node.title = fs.fields.title.value
            node.summary = fs.fields.summary.value
            node.start = fs.fields.start.value
            node.finish = fs.fields.finish.value
            node.node_user_id = current_user().id

            meta.Session.add(node)
            meta.Session.commit()
            flash(u'Событие успешно добавлено')
            return redirect_to(node.url())

        c.form = fs
        c.fs = fs.fields

        if is_ajax():
            result = render('/event/new_partial.html')
        else:
            result = render('/event/new.html')
        if request.POST:
            result = fs.htmlfill(result)
        return result

    def edit(self, id):
        node = self._get_row(model.Event, id)
        self._check_access(node)

        fs = EventForm('event-edit')

        if request.POST and fs.fields.cancel.id in request.POST:
            return redirect_to(node.url())

        if request.POST and fs.is_valid(request.POST):
            node.title = fs.fields.title.value
            node.summary = fs.fields.summary.value
            node.start = fs.fields.start.value
            node.finish = fs.fields.finish.value

            meta.Session.commit()
            flash(u'Информация о событии успешно сохранена')
            return redirect_to(node.url())

        if not request.POST:
            fs.set_values({
                'title': node.title,
                'start': node.start.strftime(DATE_FORMAT),
                'finish': node.finish.strftime(DATE_FORMAT),
                'summary': node.summary
            })

        c.node = node
        c.form = fs
        c.fs = fs.fields

        if is_ajax():
            result = render('/event/edit_partial.html')
        else:
            result = render('/event/edit.html')
        return fs.htmlfill(result)

    def show(self, id):
        self.is_page_back = True

        c.node = self._get_row(model.Event, id)

        if is_ajax():
            result = self.taconite(render('/event/show_partial.html'))
        else:
            result = render('/event/show.html')
        return result

    def list(self, user=None):
        self.is_page_back = True

        query = meta.Session.query(model.Event)
        if user is None:
            query = query.select_from(
                    join(model.Event, model.User,
                         model.Event.node_user_id == model.User.id
                    )
                ).filter(
                    and_(
                        model.Event.published != None,
                        model.User.nickname != 'demo'
                    )
                )
        else:
            user_query = meta.Session.query(model.User)
            try:
                user_node = user_query.filter(model.User.nickname == user).one()
            except NoResultFound:
                abort(404)

            query = query.filter(model.Event.node_user_id == user_node.id)

            if user_node.nickname != current_user().nickname:
                query = query.filter(model.Event.published != None)

        query = query.order_by(model.Event.start.desc())

        page = request.params.get('page', 1)
        if 'all' == page:
            c.nodes = query.all()
        else:
            c.nodes = paginate.Page(
                query,
                page=int(page),
                items_per_page = 3,
                **request.environ['pylons.routes_dict']
            )

        return render('event/list.html')

    def remove(self, id):
        node = self._get_row(model.Event, id)
        if 1 == node.id:
            abort(403)
        self._check_access(node)

        fs = form.DeleteAcceptForm('event-remove')

        if request.POST:
            if fs.fields.save.id in request.POST:
                meta.Session.delete(node)
                meta.Session.commit()
                flash(u'Событие успешно удалено')
                c.is_full_redirect=True
                return self._redirect_to(
                    controller='event',
                    action='list',
                    user=current_user().nickname
                )
            return redirect_to(node.url())
        else:
            c.form = fs
            if is_ajax():
                result = render('/util/delete_accept_partial.html')
            else:
                result = render('/util/delete_accept.html')
            return result


    def publish(self, id, published):
        node = self._get_row(model.Event, id)
        self._check_access(node)

        if published=='1':
            node.published = datetime.now()
            message = u'Событие успешно опубликовано'
        else:
            node.published = None
            message = u'Событие успешно сохранено как черновик'

        meta.Session.commit()
        flash(message)
        return redirect_to(node.url())
