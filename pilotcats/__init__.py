from pyramid.config import Configurator
from pyramid.exceptions import NotFound
from pyramid.view import view_config
from sphinx.websupport import WebSupport
from sphinx.websupport.errors import DocumentNotFoundError


_docsupport = None


def get_docsupport():
    return _docsupport


def setup_docsupport(srcdir, builddir):
    global _docsupport
    _docsupport = WebSupport(srcdir, builddir)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('doc', '/{docname:.*}',
                     factory=DocumentResource)
    config.scan('.')
    setup_docsupport(settings['pilotcats.srcdir'],
                     settings['pilotcats.builddir'])
    return config.make_wsgi_app()


class DocumentResource(object):
    def __init__(self, request):
        self.request = request

    @property
    def document(self):
        try:
            return get_docsupport().get_document(self.request.matchdict['docname'])
        except DocumentNotFoundError:
            raise NotFound


@view_config(route_name='doc',
             renderer='doc.jinja2')
def doc_view(request):
    return dict(document=request.context.document)
