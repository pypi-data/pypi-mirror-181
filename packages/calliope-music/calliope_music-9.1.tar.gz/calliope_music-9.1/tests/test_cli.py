# Calliope
# Copyright (C) 2017-2018  Sam Thursfield <sam@afuera.me.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import unittest.mock

import pytest


def test_beets(cli):
    result = cli.run(['beets'])
    assert result.exit_code == 0

def test_musicbrainz(cli):
    result = cli.run(['musicbrainz', '-'], input='')
    assert result.exit_code == 0


def test_play(cli):
    gi = pytest.importorskip("gi")

    result = cli.run(['play', '-', '--output', '/dev/null'])
    assert result.exit_code == 0


def test_shuffle(cli):
    result = cli.run(['shuffle', '-'])
    assert result.exit_code == 0


def test_spotify(cli):
    pytest.importorskip("spotipy")
    pytest.importorskip("cachecontrol")

    with unittest.mock.patch('calliope.spotify.SpotifyContext'):
        result = cli.run(['--verbosity', '3', 'spotify'])
        assert result.exit_code == 0
        result = cli.run(['--verbosity', '3', 'spotify', 'export'])
        assert result.exit_code == 0
        result = cli.run(['--verbosity', '3', 'spotify', 'resolve', '-'], input='')
        assert result.exit_code == 0


def test_stat(cli):
    result = cli.run(['stat', '-'])
    assert result.exit_code == 0


def test_suggest(cli):
    result = cli.run(['suggest'])
    assert result.exit_code == 0


def test_sync(cli):
    result = cli.run(['sync', '--target=/tmp', '-'])
    assert result.exit_code == 0


def test_tracker(cli):
    result = cli.run(['tracker'])
    assert result.exit_code == 0
