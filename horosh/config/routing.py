"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper


def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'], explicit=True)
    map.minimization = True

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE
    map.connect('/login', controller='util', action='login')
    map.connect('/logout', controller='util', action='logout')

    map.connect('demo', '/demo',
        controller='util', action='demo'
    )
    map.connect('/demo/up',
        controller='util', action='demo_up'
    )

    # Article
    map.connect('/a/{path}', controller='article', action='show')

    map.connect('/article-{id}/do/published={published}',
        controller='article', action='publish',
        requirements=dict(id='\d*', published='0|1')
    )
    map.connect('articles', '/articles', controller='article', action='list')
    map.connect('pulse', '/pulse/{action}',
        controller='article', action='list', label='pulse'
    )

    # Events
    map.connect('/', controller='event', action='list')
    map.connect('user', '/~{user}', controller='event', action='list')
    map.connect('/event-{id}-{title}',
        controller='event', action='show',
        requirements=dict(event_id='\d*')
    )
    map.connect('/event-{id}/do/published={published}',
        controller='event', action='publish',
        requirements=dict(id='\d*', published='0|1')
    )

    # Report for event
    map.connect('/event-{event_id}/add/report',
        controller='report', action='new',
        requirements=dict(event_id='\d*')
    )
    map.connect('/report-{id}/for/event-{event_id}-{title}',
        controller='report', action='show',
        requirements=dict(event_id='\d*', id='\d*')
    )

    # Person for event
    map.connect('/event-{event_id}/add/person',
        controller='person', action='new',
        requirements=dict(event_id='\d*')
    )

    map.connect('/event-{event_id}/add/album',
        controller='album', action='new',
        requirements=dict(event_id='\d*')
    )
    map.connect('/person-{id}/avatar.jpg',
        controller='person', action='avatar',
        requirements=dict(event_id='\d*')
    )
    map.connect('/album-{id}/{gallery_id}',
        controller='album', action='show',
        requirements=dict(id='\d*', gallery_id='gallery-\d*')
    )

    map.connect('/{controller}-{id}/{action}',
        action='show', requirements=dict(id='\d*')
    )
    map.connect('/{controller}/{action}')

    return map
