import re

import colander


FILENAME_REGEXP = re.compile(r'[a-zA-Z0-9_.]+')


def filename_validator(node, value):
    if not FILENAME_REGEXP.match(value):
        raise colander.Invalid(
            node,
            msg='Provided file name was not correct.'
                'Construct the name by alphanumeric or underscore only.'
        )


def filetype_validator(node, value):
    choices = ('dir', 'doc')
    if not value in choices:
        raise colander.Invalid(
            node,
            msg='Expected file type is dir or doc'
        )


class FileCreationSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(),
                               validator=filename_validator)
    type = colander.SchemaNode(colander.String(),
                               validator=filetype_validator)
    body = colander.SchemaNode(colander.String(),
                               missing='')


class DocUpdateSchema(colander.MappingSchema):
    body = colander.SchemaNode(colander.String(),
                               missing='')
