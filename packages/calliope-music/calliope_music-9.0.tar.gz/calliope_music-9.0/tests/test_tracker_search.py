# Calliope
# Copyright (C) 2018,2020  Sam Thursfield <sam@afuera.me.uk>
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

import pytest
gi = pytest.importorskip("gi")
gi.require_version('Tracker', '3.0')
from gi.repository import GLib
from gi.repository import Tracker

import trackertestutils.sandbox
import trackertestutils.storehelper

import mutagen.oggvorbis
import pytest

import logging
import pathlib
import os
import shutil
import tempfile
import urllib.request

import calliope
import testutils


@pytest.fixture(scope='module')
def tracker_miner_fs_sandbox():
    '''Private instance of tracker-miner-fs.'''
    store_tmpdir = tempfile.mkdtemp(prefix='tracker-indexed-tmpdir')
    extra_env = {}
    extra_env['XDG_DATA_HOME'] = '%s/data/' % store_tmpdir
    extra_env['XDG_CONFIG_HOME'] = '%s/config/' % store_tmpdir
    extra_env['XDG_CACHE_HOME'] = '%s/cache/' % store_tmpdir
    extra_env['XDG_RUNTIME_DIR'] = '%s/run/' % store_tmpdir

    # This tmpdir goes in cwd because paths under /tmp are ignored for indexing
    index_recursive_tmpdir = tempfile.mkdtemp(prefix='tracker-indexed-tmpdir', dir=os.getcwd())
    index_recursive_directories = [index_recursive_tmpdir]


    sandbox = trackertestutils.sandbox.TrackerSandbox(
        session_bus_config_file=None, extra_env=extra_env)
    sandbox.start()
    sandbox.set_config({
        'org.freedesktop.Tracker3.Miner.Files': {
            'index-applications': GLib.Variant('b', False),
            'index-recursive-directories': GLib.Variant('as', [index_recursive_tmpdir]),
            'index-single-directories': GLib.Variant('as', []),
            'initial-sleep': GLib.Variant('i', 0),
        }
    })
    sandbox.index_recursive_tmpdir = index_recursive_tmpdir
    yield sandbox
    sandbox.stop()
    shutil.rmtree(index_recursive_tmpdir)
    shutil.rmtree(store_tmpdir)


@pytest.fixture(scope='function')
def tracker_cli(tracker_miner_fs_sandbox):
    '''Fixture for testing through the `cpe` commandline interface.'''
    dbus_address = tracker_miner_fs_sandbox.get_session_bus_address()
    yield testutils.Cli(prepend_args=['--verbosity', '3', 'tracker'],
                        extra_env={ 'DBUS_SESSION_BUS_ADDRESS': dbus_address },
                        isolate_xdg_dirs=False)


def store_helper(sandbox):
    MINER_FS = 'org.freedesktop.Tracker3.Miner.Files'
    conn = Tracker.SparqlConnection.bus_new(MINER_FS, None, sandbox.get_session_bus_connection())
    helper = trackertestutils.storehelper.StoreHelper(conn)
    return helper


OGG_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'empty.ogg')
def create_ogg(path, helper, artist, title, album=None, tracknumber=None):
    filename = '{} - {}.ogg'.format(artist, title)
    path = path.joinpath(filename)
    shutil.copy(OGG_TEMPLATE_PATH, path)

    template = mutagen.oggvorbis.OggVorbis(path)
    template.tags['ARTIST'] = artist
    template.tags['TITLE'] = title
    if album:
        template.tags['ALBUM'] = album
    if tracknumber:
        template.tags['TRACKNUMBER'] = str(tracknumber)

    def escape(s):
        return Tracker.sparql_escape_string(s)

    template.save()
    audio_graph = 'http://tracker.api.gnome.org/ontology/v3/tracker#Audio'
    helper.ensure_resource(
        audio_graph,
        'a nmm:MusicPiece ; '
        '    nie:title "{}" ; '
        '    nmm:artist/nmm:artistName "{}"'.format(escape(title), escape(artist)),
        timeout=30)


@pytest.fixture(scope="module")
def musicdir_real(tracker_miner_fs_sandbox):
    '''Fixture providing a set of tagged audio files with real names.'''

    helper = store_helper(tracker_miner_fs_sandbox)
    path = pathlib.Path(tracker_miner_fs_sandbox.index_recursive_tmpdir)
    create_ogg(path, helper, 'Arctic Monkeys', 'Four Stars', album='Tranquility Bay Hotel & Casino')
    create_ogg(path, helper, 'The Pixies', 'Monkey Gone To Heaven')
    create_ogg(path, helper, 'Babar Luck & The Philosophers High', 'The Unofficial Mayor of London Town')
    create_ogg(path, helper, 'Fishbone', '"Simon Says" The Kingpin')

    # This track name contains Unicode char U+2019 'Right Single Quotation Mark'
    # and not the ASCII single quote mark.
    create_ogg(path, helper, 'The Mighty Mighty Bosstones', 'Don’t Know How to Party')
    return str(path)


def test_resolve_strips_punctuation(tracker_cli, tmpdir, musicdir_real):
    playlist = [
        {'creator': 'The Mighty Mighty Bosstones',
         'title': 'Don\'t Know How To Party'},
        {'creator': 'Babar Luck & The Philosopher’s High',
         'title': 'The Unofficial Mayor of London Town'},
        {'creator': 'Fishbone',
         'title': '"Simon Says" The Kingpin'}
    ]
    result = tracker_cli.run(['resolve-content', '-'], input_playlist=playlist)
    result.assert_success()

    playlist = result.json()
    assert len(playlist) == 3
    assert calliope.uri_to_path(playlist[0]['location']).exists()
    assert calliope.uri_to_path(playlist[1]['location']).exists()
    assert calliope.uri_to_path(playlist[2]['location']).exists()


def test_search(tracker_cli, tmpdir, musicdir_real):
    result = tracker_cli.run(['search', 'Monkey*'])
    result.assert_success()

    playlist = result.json()
    assert len(playlist) == 2
