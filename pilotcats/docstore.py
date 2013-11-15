"""
Storing/Providing documentation.
"""
import os

from sphinx.websupport import WebSupport


_docstore = None


def setup_docstore(storedir):
    global _docstore
    _docstore = DocStore(storedir)


def get_docstore():
    return _docstore


def get_document(docname, path):
    return get_docstore()[docname].get_document(path)


class DocumentWasNotStored(Exception):
    pass


class DocStore(object):
    def __init__(self, storedir, source_dir='source', build_dir='build/web'):
        self.storedir = storedir
        self.source_dir = source_dir
        self.build_dir = build_dir

    def __getitem__(self, item):
        target_doc_dir = os.path.join(self.storedir, item)

        if os.path.exists(target_doc_dir):
            srcdir = os.path.join(target_doc_dir, self.source_dir)
            builddir = os.path.join(target_doc_dir, self.build_dir)
            return WebSupport(srcdir, builddir)
        else:
            raise DocumentWasNotStored

    @property
    def docnames(self):
        return os.listdir(self.storedir)
