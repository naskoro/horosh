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
    map.connect('/event/{event_id}/add/person', 
        controller='person', action='new',
        requirements=dict(event_id='\d*')
    )
    map.connect('/event/{event_id}/edit/person/{id}', 
        controller='person', action='edit',
        requirements=dict(event_id='\d*', id='\d*')
    )
    map.connect('/event/{event_id}/remove/person/{id}', 
        controller='person', action='remove',
        requirements=dict(event_id='\d*', id='\d*')
    )

    map.connect('/event/{event_id}/add/album', 
        controller='album', action='new',
        requirements=dict(event_id='\d*')
    )
    #map.connect('/event/{event_id}/edit/album/{id}', 
    #    controller='album', action='edit',
    #    requirements=dict(event_id='\d*', id='\d*')
    #)
    map.connect('/event/{event_id}/remove/album/{id}', 
        controller='album', action='remove',
        requirements=dict(event_id='\d*', id='\d*')
    )

    
    map.connect('/{controller}/{id}/{action}', action='show', requirements=dict(id='\d*'))
    map.connect('/{controller}/{action}')
    

    return map
