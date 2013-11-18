from pyramid.config import Configurator

from pilotcats import docstore


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('top', '/')
    config.add_route('docstatic', '/docstatic/{docname}/{filetype:_static|_sources}/*subpath',
                     factory='pilotcats.resources.static_file_resource_factory')
    config.add_route('admin', '/admin/{docname}/*traverse',
                     factory='pilotcats.resources.source_root_factory')
    config.add_route('doc', '/docs/{docname}/{docpath:.*}',
                     factory='pilotcats.resources.document_resource_factory')
    config.scan('.views')
    docstore.setup_docstore(settings['pilotcats.storedir'])
    return config.make_wsgi_app()
