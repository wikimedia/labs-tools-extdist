#!/usr/bin/env python

"""
Basic integration tests for the tarball
generator.

Requires an internet connection and that
git is installed.
"""

import os
import unittest

from nightly import TarballGenerator


class TarballGeneratorTest(unittest.TestCase):
    def get_generator(self):
        path = os.path.dirname(os.path.abspath(__file__))
        return TarballGenerator({
            'API_URL': 'https://www.mediawiki.org/w/api.php',
            'DIST_PATH': path + '/dist',
            'GIT_URL': 'https://gerrit.wikimedia.org/r/mediawiki/extensions/%s',
            'LOG_FILE': 'extdist.log',
            'SRC_PATH': path + '/src',
            'PID_FILE': 'extdist.pid',
            })

    def test_supported_versions(self):
        gen = self.get_generator()
        self.assertIn('master', gen.supported_versions)

    def test_extension_list(self):
        """
        Testing for every extension is impossible, but
        let's assume that some of them exist
        """
        gen = self.get_generator()
        self.assertIn('MassMessage', gen.extension_list)
        self.assertIn('VisualEditor', gen.extension_list)
        self.assertIn('ExtensionDistributor', gen.extension_list)

    def test_shell_exec(self):
        gen = self.get_generator()
        self.assertEqual('hi\n', gen.shell_exec(['echo', 'hi']))
        self.assertIn('git version', gen.shell_exec(['git', '--version']))


if __name__ == '__main__':
    unittest.main()
