#!/usr/bin/env python
"""
nightly.py - tarball creator

This is a script that creates tarballs
for MediaWiki extensions based on the
configuration in conf.py. It accepts
one optional argument:

* --all: Generate tarballs for all extensions.

By default, it generates only the tarball for the
VisualEditor extension. This will change in the future
when debugging becomes less rare.
"""

import glob
import json
import logging
import os
import subprocess
import sys
import urllib

import conf


def fetch_all_extensions():
    """
    Returns raw text of extension list,
    should not be called directly
    """
    logging.debug('Fetching list of all extensions...')
    req = urllib.urlopen(get_extension_list())
    text = req.read()
    req.close()
    return text


def get_all_extensions(update=False):
    """
    Returns a list of all extension names,
    possibly using a cached list locally
    """
    fname = os.path.join(conf.SRC_PATH, 'extension-list')
    if update or not os.path.exists(fname):
        with open(fname, 'w') as f:
            exts = fetch_all_extensions()
            f.write(exts)
    else:
        with open(fname, 'r') as f:
            exts = f.read()

    return exts.strip().splitlines()


def get_supported_branches():
    if conf.SUPPORTED_VERSIONS is None:
        conf.SUPPORTED_VERSIONS = get_extension_config()['versions']
    return conf.SUPPORTED_VERSIONS


def get_extension_list():
    if conf.EXT_LIST is None:
        conf.EXT_LIST = get_extension_config()['extension-list']
    return conf.EXT_LIST


def fetch_extension_config():
    logging.debug('Fetching ExtensionDistributor config from API...')
    data = {
        'action': 'query',
        'meta': 'siteinfo',
        'format': 'json',
    }
    req = urllib.urlopen(conf.API_URL, data)
    resp = json.loads(req.read())
    return {
        'versions': resp['query']['general']['extensiondistributor']['snapshots'],
        'extension-list': resp['query']['general']['extensiondistributor']['list']
    }


def get_extension_config(update=False):
    fname = os.path.join(conf.SRC_PATH, 'mw-conf.json')
    if update or not os.path.exists(fname):
        with open(fname, 'w') as f:
            e_config = fetch_extension_config()
            json.dump(e_config, f)
    else:
        with open(fname, 'r') as f:
            e_config = json.load(f)

    return e_config


def shell_exec(args, **kwargs):
    """
    Shortcut wrapper to execute a shell command

    >>> shell_exec(['ls', '-l'])
    """
    return subprocess.check_output(args, **kwargs)


def update_extension(ext):
    """
    Fetch an extension's updates, and
    create new tarballs if needed
    """
    full_path = os.path.join(conf.SRC_PATH, ext)
    logging.info('Starting update for %s' % ext)
    if not os.path.exists(full_path):
        os.chdir(conf.SRC_PATH)
        logging.debug('Cloning %s' % ext)
        shell_exec(['git', 'clone', conf.GIT_URL % ext, ext])
        pass
    for branch in get_supported_branches():
        os.chdir(full_path)
        logging.info('Creating %s for %s' %(branch, ext))
        # Update remotes
        shell_exec(['git', 'fetch'])
        try:
            # Could fail if repo is empty
            shell_exec(['git', 'reset', '--hard', 'origin/master'])
            # Checkout the branch
            shell_exec(['git', 'checkout', 'origin/%s' % branch])
        except subprocess.CalledProcessError:
            logging.error('could not checkout origin/%s' % branch)
            continue
        # Sync submodules in case their urls have changed
        shell_exec(['git', 'submodule', 'sync'])
        # Update them, initializing new ones if needed
        shell_exec(['git', 'submodule', 'update', '--init'])
        # Gets short hash of HEAD
        rev = shell_exec(['git', 'rev-parse', '--short', 'HEAD']).strip()
        tarball_fname = '%s-%s-%s.tar.gz' % (ext, branch, rev)
        if os.path.exists(os.path.join(conf.DIST_PATH, tarball_fname)):
            logging.debug('No updates to branch, tarball already exists.')
            continue
        # Create a 'version' file with basic info about the tarball
        with open('version', 'w') as f:
            f.write('%s: %s\n' %(ext, branch))
            f.write(shell_exec(['date', '+%Y-%m-%dT%H:%M:%S']) + '\n')  # TODO: Do this in python
            f.write(rev + '\n')
        old_tarballs = glob.glob(os.path.join(conf.DIST_PATH, '%s-%s-*.tar.gz' %(ext, branch)))
        logging.debug('Deleting old tarballs...')
        for old in old_tarballs:
            # FIXME: Race condition, we should probably do this later on...
            os.unlink(old)
        os.chdir(conf.SRC_PATH)
        # Finally, create the new tarball
        shell_exec(['tar', 'czPf', tarball_fname, ext])
    logging.debug('Moving new tarballs into dist/')
    tarballs = glob.glob(os.path.join(conf.SRC_PATH, '*.tar.gz'))
    for tar in tarballs:
        fname = tar.split('/')[-1]
        os.rename(tar, os.path.join(conf.DIST_PATH, fname))
    logging.info('Finished update for %s' % ext)


def main():
    """
    Updates all extensions
    """
    extensions = get_all_extensions(update=True)
    logging.info('Starting update of all extensions...')
    for ext in extensions:
        update_extension(ext)
    logging.info('Finished update of all extensions!')


if __name__ == '__main__':
    if '--all' in sys.argv:
        main()
    else:
        update_extension('VisualEditor')
