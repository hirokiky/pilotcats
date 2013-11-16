from pilotcats import docstore


def source_root_factory(request):
    return docstore.get_docstore().get_source(request.matchdict['docname'])


def static_file_resource_factory(request):
    return docstore.StaticFileResource(request.matchdict['docname'],
                                       request.matchdict['filetype'])


def document_resource_factory(request):
    return docstore.DocumentResource(request.matchdict['docname'],
                                     request.matchdict['docpath'])
