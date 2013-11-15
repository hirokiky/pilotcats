import sys

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pilotcats import docstore


def main(argv=sys.argv):
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    docstore.setup_docstore(settings['pilotcats.storedir'])
    docstore.get_docstore()[argv[2]].build()
