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


@view_config(route_name='api_tree',
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

    filetype = conditions['type']
    if filetype == 'doc':
        name = conditions['name'] + '.rst'
        request.context.create_doc(name,
                                   conditions['body'])
    elif filetype == 'src':
        name = conditions['name']
        request.context.create_dir(name)
    else:
        request.response.status = 400
        return {}

    link_for_child = request.route_url('api_tree',
                                       docname=request.matchdict['docname'],
                                       traverse=request.matchdict['traverse'] + [name])

    request.response.status = 201

    return dict(type=filetype,
                name=name,
                link=link_for_child)


@view_config(route_name='api_tree',
             renderer='json',
             request_method=['PUT'],
             context='pilotcats.docstore.FileResource')
def doc_update_view(request):
    schema = pilotcats_schema.DocUpdateSchema()
    try:
        conditions = schema.deserialize(request.PUT)
    except colander.Invalid as e:
        request.response.status = 400
        return dict(errors=e.asdict())
    request.context.update_body(conditions['body'])
    request.response.status = 204
    return {}


@view_config(route_name='api_tree',
             renderer='json',
             request_method=['DELETE'],
             context='pilotcats.docstore.DirResource')
def doc_dir_delete_view(request):
    request.context.delete_file()
    return dict(type='dir')


@view_config(route_name='api_tree',
             renderer='json',
             request_method=['DELETE'],
             context='pilotcats.docstore.FileResource')
def doc_file_delete_view(request):
    request.context.delete_file()
    return dict(type='src')


@view_config(route_name='api_tree',
             renderer='json',
             request_method=['GET'],
             context='pilotcats.docstore.DirResource')
def tree_view(request):
    return dict(type='dir',
                content=list(request.context))


@view_config(route_name='api_tree',
             renderer='json',
             request_method=['GET'],
             context='pilotcats.docstore.FileResource')
def file_view(request):
    with request.context as f:
        content = f.read()
    return dict(type='src',
                content=content)
