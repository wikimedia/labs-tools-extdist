#!/usr/bin/env python

SRC_PATH = '/srv/src/extensions'
#SRC_PATH = '/Users/km/projects/extdist/src/extensions'
DIST_PATH = '/srv/dist'
#DIST_PATH = '/Users/km/projects/extdist/dist'
GIT_URL = 'https://github.com/wikimedia/mediawiki-extensions-%s'
SUPPORTED_VERSIONS = ['master', 'REL1_23', 'REL1_22', 'REL1_21', 'REL1_20', 'REL1_19']  # TODO: fetch from API
EXT_LIST = 'https://gerrit.wikimedia.org/mediawiki-extensions.txt'  # TODO: fetch from API
URL_ENDPOINT = 'https://extdist.wmflabs.org/dist/%s'
