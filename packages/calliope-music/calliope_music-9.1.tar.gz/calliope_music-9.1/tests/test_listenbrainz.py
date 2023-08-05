# Calliope
# Copyright (C) 2022  Sam Thursfield <sam@afuera.me.uk>
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


"""Tests for the `cpe listenbrainz` command."""


import pytest

pytest.importorskip("calliope.subprojects.pylistenbrainz")

import json
import logging
import os
import pathlib
import threading
import urllib.parse
import wsgiref.util

import calliope.listenbrainz
import testutils


@pytest.fixture
def mock_server(monkeypatch):
    '''Pretend to be a Listenbrainz server.'''

    template_path = pathlib.Path(os.path.dirname(__file__), 'data')

    class MockListenBrainzServer(testutils.MockWebServer):
        def __init__(self):
            super(MockListenBrainzServer, self).__init__(self.handle_request)
            self.listen_count = 10
            with open(template_path.joinpath('listenbrainz.listens.json')) as f:
                self.listens = json.load(f)['listens']

        def handle_request(self, environ, start_response):
            wsgiref.util.setup_testing_defaults(environ)

            path = environ['PATH_INFO']
            params = urllib.parse.parse_qs(environ['QUERY_STRING'])
            logging.debug("Test server: Got request at %s with params: %s", path, params)

            if path == '/1/user/samthursfield2/playlists':
                with open(template_path.joinpath('listenbrainz.user_playlists.json')) as f:
                    data = json.load(f)
                return self.json_response(start_response, data)
            elif path == '/1/playlist/9fd69aa9-fba8-452c-9212-19a0c6d5b2d0':
                with open(template_path.joinpath('listenbrainz.playlist_9fd6.json')) as f:
                    data = json.load(f)
                return self.json_response(start_response, data)
            else:
                return self.json_not_found_response(start_response)

    server = MockListenBrainzServer()
    server.start()

    monkeypatch.setattr('calliope.subprojects.pylistenbrainz.client.API_BASE_URL', server.base_uri())

    # Override page size so we can limit the size of our test data.
    monkeypatch.setattr('calliope.listenbrainz.api.MAX_ITEMS_PER_GET', 5)

    return server


def test_get_playlists(mock_server):
    cli = testutils.Cli(prepend_args=[
        '--verbosity', '3', 'listenbrainz', '--user=samthursfield2'
    ])

    playlist_series = cli.run(['export']).json()
    assert len(playlist_series) == 31
    assert playlist_series[0]['playlist.title'] == 'Top recordings of 2020 for samthursfield2'
    assert playlist_series[0]['listenbrainz.playlist.last_modified_at'] == '2020-12-27T16:34:11.158302+00:00'
    assert playlist_series[0]['creator'] == 'The Mighty Mighty Bosstones'
    assert playlist_series[0]['listenbrainz.artist_identifiers'] == ['779353f3-6401-4cda-a8a2-6fd3ec9bc11b']
