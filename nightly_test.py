#!/usr/bin/env python

"""
Basic integration tests for the tarball
generator.

Requires an internet connection and that
git is installed.
"""

import os

from nightly import TarballGenerator


class TestTarballGenerator:
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
        assert 'master' in gen.supported_versions

    def test_repo_list(self):
        """
        Testing for every extension/skin is impossible, but
        let's assume that some of them exist
        """
        gen = self.get_generator('extensions')
        assert 'MassMessage' in gen.repo_list
        assert 'VisualEditor' in gen.repo_list
        assert 'ExtensionDistributor' in gen.repo_list

    def test_skin_repo_list(self):
        skin_gen = self.get_generator('skins')
        assert 'CologneBlue' in skin_gen.repo_list
        assert 'GreyStuff' in skin_gen.repo_list
        assert 'MonoBook' in skin_gen.repo_list

    def test_shell_exec(self):
        gen = self.get_generator('extensions')
        assert 'hi\n' == gen.shell_exec(['echo', 'hi'])
        assert 'git version' in gen.shell_exec(['git', '--version'])
