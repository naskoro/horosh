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
    map.connect('/', controller='event', action='list')
    
    map.connect('/login', controller='util', action='login')
    map.connect('/logout', controller='util', action='logout')
    
    # Article
    map.connect('/a/{path}', controller='article', action='show')
    
    map.connect('/article-{id}/do/published={published}', 
        controller='article', action='publish',
        requirements=dict(id='\d*', published='0|1')
    )
    map.connect('article_list', '/article/list', controller='article', action='list')
    
    # Events
    map.connect('/~{user}', controller='event', action='list')
    map.connect('/event-{id}-{title}', 
        controller='event', action='show',
        requirements=dict(event_id='\d*')
    )
    map.connect('/event-{event_id}-{title}/report-{id}', 
        controller='report', action='show',
        requirements=dict(event_id='\d*', id='\d*')
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
    map.connect('/event-{event_id}/edit/report-{id}', 
        controller='report', action='edit',
        requirements=dict(event_id='\d*', id='\d*')
    )
    map.connect('/event-{event_id}/remove/report-{id}', 
        controller='report', action='remove',
        requirements=dict(event_id='\d*', id='\d*')
    )
    
    # Person for event
    map.connect('/event-{event_id}/add/person', 
        controller='person', action='new',
        requirements=dict(event_id='\d*')
    )
    map.connect('/event-{event_id}/edit/person-{id}', 
        controller='person', action='edit',
        requirements=dict(event_id='\d*', id='\d*')
    )
    map.connect('/event-{event_id}/remove/person-{id}', 
        controller='person', action='remove',
        requirements=dict(event_id='\d*', id='\d*')
    )
    
    # Album for event
    map.connect('/event-{event_id}/add/album', 
        controller='album', action='new',
        requirements=dict(event_id='\d*')
    )
    map.connect('/event-{event_id}/remove/album-{id}', 
        controller='album', action='remove',
        requirements=dict(event_id='\d*', id='\d*')
    )
    map.connect('/person-{id}/avatar.jpg',
        controller='person', action='avatar',
        requirements=dict(event_id='\d*')
    )
    
    map.connect('/{controller}-{id}/{action}', action='show', requirements=dict(id='\d*'))
    map.connect('/{controller}/{action}')
    

    return map
