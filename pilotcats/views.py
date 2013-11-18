import colander
from pyramid.static import static_view
from pyramid.view import view_config

from pilotcats import docstore
from pilotcats import schema as pilotcats_schema


@view_config(route_name='docstatic')
def doc_static_view(request):
    return static_view(request.context.static_dir_path, use_subpath=True)(request.context, request)


@view_config(route_name='top',
             renderer='top.jinja2')
def top_view(request):
    return dict(docnames=docstore.get_docstore().docnames)


@view_config(route_name='doc',
             renderer='doc.jinja2')
def doc_view(request):
    return dict(document=request.context.document,
                docglobal=request.context.docglobal)


@view_config(route_name='admin',
             renderer='json',
             request_method=['POST'],
             context='pilotcats.docstore.DirResource')
def doc_create_view(request):
    schema = pilotcats_schema.FileCreationSchema()
    try:
        conditions = schema.deserialize(request.POST)
    except colander.Invalid as e:
        request.response.status = 400
        return dict(errors=e.asdict())
    if conditions['type'] == 'doc':
        request.context.create_doc(conditions['name'] + '.rst',
                                   conditions['body'])
    else:
        request.context.create_dir(conditions['name'])

    return {}


@view_config(route_name='admin',
             renderer='json',
             request_method=['POST'],
             context='pilotcats.docstore.FileResource')
def doc_update_view(request):
    schema = pilotcats_schema.DocUpdateSchema()
    try:
        conditions = schema.deserialize(request.POST)
    except colander.Invalid as e:
        request.response.status = 400
        return dict(errors=e.asdict())
    request.context.update_body(conditions['body'])
    return {}


@view_config(route_name='admin',
             renderer='json',
             request_method=['DELETE'])
def doc_delete_view(request):
    request.context.delete_file()
    return {}


@view_config(route_name='admin',
             renderer='dirtree.jinja2',
             request_method=['GET'],
             context='pilotcats.docstore.DirResource')
def tree_view(request):
    return {}


@view_config(route_name='admin',
             renderer='dirfile.jinja2',
             request_method=['GET'],
             context='pilotcats.docstore.FileResource')
def file_view(request):
    with request.context as f:
        content = f.read()
    return dict(content=content)
