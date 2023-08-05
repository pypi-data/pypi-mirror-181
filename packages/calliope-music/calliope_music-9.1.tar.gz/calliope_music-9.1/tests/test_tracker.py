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

import testutils

# These are module-scope fixtures because they are slow to set up.
# Start a new module if you need a different fixture.

@pytest.fixture(scope='module')
def tracker_miner_fs_sandbox():
    '''Private instance of tracker-miner-fs.'''
    store_tmpdir = tempfile.mkdtemp(prefix='tracker-test-tmpdir')
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
        template.tags['ALBUMARTIST'] = artist
    if tracknumber:
        template.tags['TRACKNUMBER'] = str(tracknumber)

    audio_graph = 'http://tracker.api.gnome.org/ontology/v3/tracker#Audio'
    predicates = 'a nmm:MusicPiece ; nie:title "%s" ; nmm:artist/nmm:artistName "%s"' % (title, artist)
    with helper.await_insert(audio_graph, predicates):
        template.save()


@pytest.fixture(scope='module')
def musicdir(tracker_miner_fs_sandbox):
    '''Fixture providing a standard set of tagged audio files.'''

    helper = store_helper(tracker_miner_fs_sandbox)
    path = pathlib.Path(tracker_miner_fs_sandbox.index_recursive_tmpdir)
    create_ogg(path, helper, 'Artist 1', 'Track 1', album='Album 1', tracknumber=1)
    create_ogg(path, helper, 'Artist 1', 'Track 2', album='Album 1', tracknumber=2)
    create_ogg(path, helper, 'Artist 1', 'Track 3')
    create_ogg(path, helper, 'Artist 2', 'Track 1')
    create_ogg(path, helper, 'Artist 2', 'Track 2')
    create_ogg(path, helper, 'Artist 2', 'Track 3')
    logging.info("All data now in store!!!!")

    return str(path)


def test_resolve_content(tracker_cli, musicdir):
    logging.info("Starting test 1")
    input_playlist = [
        {
            'creator': 'Artist 1',
            'title': 'Track 1',
        }
    ]

    result = tracker_cli.run(['resolve-content', '-'], input_playlist=input_playlist)
    result.assert_success()

    expected_url = 'file://' + urllib.request.pathname2url(os.path.join(musicdir, 'Artist 1 - Track 1.ogg'))

    output_playlist = result.json()
    assert output_playlist[0]['creator'] == 'Artist 1'
    assert output_playlist[0]['title'] == 'Track 1'
    assert output_playlist[0]['tracker.location'] == expected_url


def test_expand_tracks_for_artist(tracker_cli, musicdir):
    logging.info("Starting test 2")
    input_playlist = [
        {
            'creator': 'Artist 1',
            'title': 'Track 1',
        },
        {
            'creator': 'Artist 2',
        }
    ]

    result = tracker_cli.run(['expand-tracks', '-'], input_playlist=input_playlist)
    result.assert_success()

    output_playlist = result.json()
    assert output_playlist[0]['creator'] == 'Artist 1'
    assert output_playlist[0]['title'] == 'Track 1'
    assert output_playlist[1]['creator'] == 'Artist 2'
    assert output_playlist[1]['title'] == 'Track 1'
    assert output_playlist[2]['creator'] == 'Artist 2'
    assert output_playlist[2]['title'] == 'Track 2'
    assert output_playlist[3]['creator'] == 'Artist 2'
    assert output_playlist[3]['title'] == 'Track 3'
    assert len(output_playlist) == 4


def test_expand_tracks_for_album(tracker_cli, musicdir):
    logging.info("Starting test 3")
    input_playlist = [
        {
            'creator': 'Artist 1',
            'album': 'Album 1',
        },
    ]

    result = tracker_cli.run(['expand-tracks', '-'], input_playlist=input_playlist)
    result.assert_success()

    output_playlist = result.json()
    print(output_playlist)
    assert output_playlist[0]['creator'] == 'Artist 1'
    assert output_playlist[0]['title'] == 'Track 1'
    assert output_playlist[1]['creator'] == 'Artist 1'
    assert output_playlist[1]['title'] == 'Track 2'
    assert len(output_playlist) == 2


def test_resolve_content(tracker_cli, musicdir):
    # Test that matches are case-insensitive.
    input_playlist = [
        {
            'creator': 'artist 1',
            'title': 'TRACK 1',
        },
    ]

    result = tracker_cli.run(['resolve-content', '-'], input_playlist=input_playlist)

    result.assert_success()

    output_playlist = result.json()
    print(output_playlist)
    assert output_playlist[0]['creator'] == 'artist 1'
    assert output_playlist[0]['location'].endswith('Artist%201%20-%20Track%201.ogg')
    assert len(output_playlist) == 1


def test_show(tracker_cli, musicdir):
    logging.info("Starting test 4")
    result = tracker_cli.run(['albums'])
    result.assert_success()

    collection = result.json()
    assert collection[0]['creator'] == 'Artist 1'
    assert collection[0]['album'] == 'Album 1'
    assert collection[0]['album.trackcount'] == 2
    # Unfortunately the test files are tiny and size rounds down to zero.
    assert collection[0]['tracker.size_mb'] == 0
    assert collection[0]['duration'] == 20000   # 20 seconds

    result = tracker_cli.run(['tracks'])
    result.assert_success()

    collection = result.json()
    assert collection[0]['creator'] == 'Artist 1'
    assert collection[0]['title'] == 'Track 1'
    assert collection[1]['creator'] == 'Artist 2'
    assert collection[1]['title'] == 'Track 1'
    assert collection[2]['creator'] == 'Artist 1'
    assert collection[2]['title'] == 'Track 2'
    assert collection[3]['creator'] == 'Artist 2'
    assert collection[3]['title'] == 'Track 2'
    assert collection[4]['creator'] == 'Artist 1'
    assert collection[4]['title'] == 'Track 3'
    assert collection[5]['creator'] == 'Artist 2'
    assert collection[5]['title'] == 'Track 3'
