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
    def get_generator(self, _type='extensions'):
        path = os.path.dirname(os.path.abspath(__file__))
        shortname = 'skindist' if _type == 'skins' else 'extdist'
        return TarballGenerator({
            'API_URL': 'https://www.mediawiki.org/w/api.php',
            'DIST_PATH': '%s/%s/dist' % (path, _type),
            'GIT_URL': 'https://gerrit.wikimedia.org/r/mediawiki/%s/%s' % (_type, '%s'),
            'LOG_FILE': '%s.log' % shortname,
            'SRC_PATH': '%s/%s/src' % (path, _type),
            'PID_FILE': '%s.pid' % shortname,
            }, repo_type=_type)

    def test_supported_versions(self):
        gen = self.get_generator('extensions')
        self.assertIn('master', gen.supported_versions)

    def test_repo_list(self):
        """
        Testing for every extension/skin is impossible, but
        let's assume that some of them exist
        """
        gen = self.get_generator('extensions')
        self.assertIn('MassMessage', gen.repo_list)
        self.assertIn('VisualEditor', gen.repo_list)
        self.assertIn('ExtensionDistributor', gen.repo_list)

    def test_skin_repo_list(self):
        skin_gen = self.get_generator('skins')
        self.assertIn('CologneBlue', skin_gen.repo_list)
        self.assertIn('GreyStuff', skin_gen.repo_list)
        self.assertIn('MonoBook', skin_gen.repo_list)

    def test_shell_exec(self):
        gen = self.get_generator('extensions')
        self.assertEqual('hi\n', gen.shell_exec(['echo', 'hi']))
        self.assertIn('git version', gen.shell_exec(['git', '--version']))


if __name__ == '__main__':
    unittest.main()
