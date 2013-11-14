import sys

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pilotcats import setup_docsupport, get_docsupport


def main(argv=sys.argv):
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    setup_docsupport(settings['pilotcats.srcdir'],
                     settings['pilotcats.builddir'])
    get_docsupport().build()
