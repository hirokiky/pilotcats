from pyramid.config import Configurator
from pyramid.exceptions import NotFound
from pyramid.view import view_config
from sphinx.websupport.errors import DocumentNotFoundError

from pilotcats import docstore


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('doc', '/{docname}/{docpath:.*}',
                     factory=DocumentResource)
    config.scan('.')
    docstore.setup_docstore(settings['pilotcats.storedir'])
    return config.make_wsgi_app()


class DocumentResource(object):
    def __init__(self, request):
        self.request = request

    @property
    def document(self):
        try:
            return docstore.get_document(self.request.matchdict['docname'],
                                         self.request.matchdict['docpath'])
        except (docstore.DocumentWasNotStored, DocumentNotFoundError):
            raise NotFound


@view_config(route_name='doc',
             renderer='doc.jinja2')
def doc_view(request):
    return dict(document=request.context.document)
