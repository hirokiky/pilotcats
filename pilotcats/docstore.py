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


def source_root_factory(request):
    return get_docstore().get_source(request.matchdict['docname'])


class DocumentWasNotStored(Exception):
    pass


class DocStore(object):
    def __init__(self, storedir, sourcepath='source', buildpath='build/web'):
        self.storedir = storedir
        self.sourcepath = sourcepath
        self.buildpath = buildpath

    def __getitem__(self, item):
        target_doc_dir = os.path.join(self.storedir, item)

        if os.path.exists(target_doc_dir):
            srcdir = os.path.join(target_doc_dir, self.sourcepath)
            builddir = os.path.join(target_doc_dir, self.buildpath)
            return WebSupport(srcdir, builddir,
                              staticroot='static/%s' % item)
        else:
            raise DocumentWasNotStored

    @property
    def docnames(self):
        return os.listdir(self.storedir)

    def get_source(self, dirname):
        return DirResource(os.path.join(self.storedir, dirname, self.sourcepath))

    def get_staticdir(self, docname, filetype):
        static_dir = os.path.join(self.storedir, docname, self.buildpath, 'static', filetype)
        if os.path.exists(static_dir) and os.path.isdir(static_dir):
            return static_dir
        else:
            raise DocumentWasNotStored


class DirResource(object):
    def __init__(self, path):
        if not os.path.isdir(path):
            raise ValueError('Provided item was not directory: %s' % path)
        else:
            self.path = path

    def __contains__(self, item):
        return os.path.exists(os.path.join(self.path, item))

    def __iter__(self):
        return (p for p in os.listdir(self.path))

    def __getitem__(self, item):
        filepath = os.path.join(self.path, item)
        if not os.path.exists(filepath):
            raise KeyError
        try:
            return DirResource(filepath)
        except ValueError:
            return FileResource(filepath)


class FileResource(object):
    def __init__(self, path):
        if os.path.isdir(path):
            raise ValueError('Provided item was not file: %s' % path)
        else:
            self.path = path

    def __enter__(self):
        self.file = open(self.path)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def __getitem__(self, item):
        raise KeyError
