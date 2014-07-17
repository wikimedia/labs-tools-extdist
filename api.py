#!/usr/bin/env python

import json
import os
from flask import Flask, redirect, request, send_from_directory

import conf
import nightly

app = Flask(__name__, static_url_path='')
app.debug = True


def get_link(ext, version):
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
    #return out({'foo': path})
    if path.endswith('.tar.gz'):
        # Err, do some more secure file checking
        return send_from_directory(conf.DIST_PATH, path, as_attachment=True)
    else:
        return out({'error': 'invalidfile'})


def out(j):
    return json.dumps(j)

@app.route('/')
def entry_point():
    ext = request.args.get('ext')
    version = request.args.get('version')
    if not ext and not version:
        return redirect('https://www.mediawiki.org/wiki/Special:ExtensionDistributor', code=302)
    if not version in conf.SUPPORTED_VERSIONS:
        return out({'error': 'badversion'})
    if not ext in nightly.get_all_extensions():
        return out({'error': 'badext'})

    info = get_link(ext, version)
    if type(info) == dict:
        # Error message
        return out(info)

    return redirect(info, code=302)

if __name__ == '__main__':
    app.run(debug=True)
