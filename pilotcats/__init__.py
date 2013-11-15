from pyramid.config import Configurator
from pyramid.exceptions import NotFound
from pyramid.view import view_config
from sphinx.websupport.errors import DocumentNotFoundError

from pilotcats import docstore


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('top', '/')
    config.add_route('admin', '/admin/{docname}/*traverse',
                     factory='pilotcats.docstore.source_root_factory')
    config.add_route('doc', '/docs/{docname}/{docpath:.*}',
                     factory=DocumentResource)
    config.scan('.')
    docstore.setup_docstore(settings['pilotcats.storedir'])
    return config.make_wsgi_app()


@view_config(route_name='top',
             renderer='top.jinja2')
def top_view(request):
    return dict(docnames=docstore.get_docstore().docnames)


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


@view_config(route_name='admin',
             renderer='dirtree.jinja2',
             context='pilotcats.docstore.DirResource')
def tree_view(request):
    return {}


@view_config(route_name='admin',
             renderer='dirfile.jinja2',
             context='pilotcats.docstore.FileResource')
def file_view(request):
    with request.context as f:
        content = f.read()
    return dict(content=content)
