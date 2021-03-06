# -*- coding: utf-8 -*-
"""
    Implements the quickstart fix.

    :copyright: Copyright 2011 by the RedBarrel team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import os
import codecs
from mako.template import Template


_TMPLDIR = os.path.join(os.path.dirname(__file__), 'templates')
_QUICKSTART = os.path.join(_TMPLDIR, 'quickstart.mako')
_WSGI = os.path.join(_TMPLDIR, 'app.wsgi.mako')
_SETUP_PY = os.path.join(_TMPLDIR, 'setup.py.mako')
_SETUP_CFG = os.path.join(_TMPLDIR, 'setup.cfg.mako')
_HELLO = """\
def hello(app, req):
    return "Hello world"
"""


def _filename(root, ext=''):
    finalname = root + ext
    counter = 1
    while os.path.exists(finalname):
        fname = '%s-%d' % (root, counter)
        finalname = fname + ext
        counter += 1
    return finalname


def _write_tmpl(tmpl, root, ext, data):
    with open(tmpl) as f:
        res = Template(f.read()).render(**data)

    filename = _filename(root, ext)
    with codecs.open(filename, encoding='utf-8', mode='w') as f:
        f.write(res)
    return filename


def quickstart():
    data = {}
    data['name'] = raw_input("Name of the project: ")
    data['description'] = raw_input("Description: ")
    data['version'] = raw_input("Version [1.0]: ")
    data['home'] = raw_input("Home page of the project: ")
    data['author'] = raw_input("Author: ")
    data['email'] = raw_input("Author e-mail: ")

    for key in data.keys():
        data[key] = data[key].decode("utf-8")

    if not data['version']:
        data['version'] = "1.0"

    # let's create the package
    pkg_name = data['name'].lower().replace(' ', '_')[:8]
    pkg_name = _filename(pkg_name)
    os.mkdir(pkg_name)
    with open(os.path.join(pkg_name, '__init__.py'), 'w') as f:
        f.write('# generated by RedBarrel')

    with open(os.path.join(pkg_name, 'hello.py'), 'w') as f:
        f.write(_HELLO)

    data['pkg_name'] = pkg_name

    # ... the RBR file
    file_root = data['name'].lower().replace(' ', '-')[:8]
    rbr = _write_tmpl(_QUICKSTART, file_root, '.rbr', data)
    data['rbr'] = rbr

    # ...the setup.py
    _write_tmpl(_SETUP_PY, 'setup', '.py', data)

    # ...the setup.cfg
    _write_tmpl(_SETUP_CFG, 'setup', '.cfg', data)

    # ... and finally, the app.wsgi file
    wsgi_data = {'filename': rbr}
    wsgiapp = os.path.join(pkg_name, 'wsgiapp')
    _write_tmpl(_WSGI, wsgiapp, '.py', wsgi_data)
    print('App generated. Run your app with "rb-run %s"' % rbr)
