import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='pilotcats',
    version='0.0',
    packages=find_packages(),
    url='https://github.com/hirokiky/pilotcats',
    license='MIT',
    author='hirokiky',
    author_email='hirokiky@gmail.com',
    description='An app for writing docs through web.',
    long_description=README,
    install_requires=[
        'Sphinx==1.2b3',
        'pyramid==1.5a2',
        'pyramid-jinja2==1.9',
        'SQLAlchemy==0.8.3',
        'waitress==0.8.7',
    ],
    entry_points="""\
    [paste.app_factory]
    main = pilotcats:main
    [console_scripts]
    builddoc = pilotcats.scripts.builddoc:main
    """
)
