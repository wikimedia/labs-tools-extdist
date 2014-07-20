#!/usr/bin/env python

SRC_PATH = '/srv/src/extensions'
#SRC_PATH = '/Users/km/projects/extdist/src/extensions'
DIST_PATH = '/srv/dist'
#DIST_PATH = '/Users/km/projects/extdist/dist'
GIT_URL = 'https://github.com/wikimedia/mediawiki-extensions-%s'
SUPPORTED_VERSIONS = None  # lazy-init
EXT_LIST = None  # lazy-init
URL_ENDPOINT = 'https://extdist.wmflabs.org/dist/%s'
API_URL = 'https://www.mediawiki.org/w/api.php'
