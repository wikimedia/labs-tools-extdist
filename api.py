#!/usr/bin/env python
"""
api.py - Webserver

This webserver is designed to mimic Github's
tarball API. It exposes two entry points:

* / - accepts "version" and "ext" parameters,
      API entry point

* /dist - serves generated tarballs to users
"""
import json
import os
from flask import Flask, redirect, request, send_from_directory

import conf
import nightly

app = Flask(__name__, static_url_path='')
app.debug = True


def get_link(ext, version):
    """
    Get the /dist/ link to a tarball, given
    extension name and version.
    Returns a dictionary if tarball doesn't
    exist.
    """
    files = os.listdir(conf.DIST_PATH)
    f = False
    for f in files:
        # VisualEditor-REL1_23-9883566.tar.gz
        if f.startswith('%s-%s' % (ext, version)):
            break

    if f is False:
        return {'error': 'notfound'}
    else:
        return conf.URL_ENDPOINT % f

@app.route('/dist/<path:path>')
def serve_files(path):
    """
    Serves tarballs. flask will only allow files in
    conf.DIST_PATH to be accessed.
    """
    if path.endswith('.tar.gz'):
        # Err, do some more secure file checking
        return send_from_directory(conf.DIST_PATH, path, as_attachment=True)
    else:
        return out({'error': 'invalidfile'})


def out(j):
    """
    Wrapper for error message formatter
    In the future we might want to make
    this look pretty or something.
    """
    return json.dumps(j)

@app.route('/')
def entry_point():
    ext = request.args.get('ext')
    version = request.args.get('version')
    if not ext and not version:
        # Our home page is a redirect to mw.o
        return redirect('https://www.mediawiki.org/wiki/Special:ExtensionDistributor', code=302)
    if not version in nightly.get_supported_branches():
        # Check version is a "supported" one
        return out({'error': 'badversion'})
    if not ext in nightly.get_all_extensions():
        # Check extension name is a valid one
        return out({'error': 'badext'})

    info = get_link(ext, version)
    if type(info) == dict:
        # Error message
        return out(info)

    # Redirect to the tarball
    return redirect(info, code=302)

if __name__ == '__main__':
    app.run(debug=True)
