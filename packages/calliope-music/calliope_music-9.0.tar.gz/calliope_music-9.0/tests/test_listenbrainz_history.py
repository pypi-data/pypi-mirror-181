# Calliope
# Copyright (C) 2021  Sam Thursfield <sam@afuera.me.uk>
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


"""Tests for the `cpe listenbrainz-history` command."""


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

            if path == '/1/user/calliope_test/listen-count':
                data = dict(payload=dict(count=self.listen_count))
                return self.json_response(start_response, data)
            elif path == '/1/user/calliope_test/listens':
                count = int(params['count'][0])
                if 'max_ts' in params:
                    max_ts = int(params.get('max_ts')[0])
                else:
                    max_ts = None
                listens = []
                for l in self.listens:
                    if max_ts is None or l['listened_at'] < max_ts:
                        listens.append(l)
                    if len(listens) >= count:
                        break
                data = dict(
                    payload=dict(
                        count=len(listens),
                        latest_listen_ts=self.listens[0]['listened_at'],
                        listens=listens,
                        user_id='samthursfield2'
                    )
                )
                return self.json_response(start_response, data)
            else:
                return self.json_not_found_response()

    server = MockListenBrainzServer()
    server.start()

    monkeypatch.setattr('calliope.subprojects.pylistenbrainz.client.API_BASE_URL', server.base_uri())

    # Override page size so we can limit the size of our test data.
    monkeypatch.setattr('calliope.listenbrainz.api.MAX_ITEMS_PER_GET', 5)

    return server


def test_full_sync(mock_server):
    cli = testutils.Cli(prepend_args=[
        '--verbosity', '3', 'listenbrainz-history', '--user=calliope_test'
    ])
    result = cli.run(['listens'])

    result.assert_success()
    listens = result.json()
    assert len(listens) == 100


def test_partial_sync(mock_server, tmpdir):
    history = calliope.listenbrainz.listens.load(username='calliope_test',
                                                 cachedir=tmpdir)

    # Sync the first page, then cancel
    op = history.prepare_sync()
    for page in op.pages():
        op.process_page(page)
        break

    # Sync again, we should only sync second page.
    op = history.prepare_sync()
    assert len(op.pages()) == 1
    for page in op.pages():
        op.process_page(page)

    listens = list(history.listens())
    assert len(listens) == 10


def test_sync_incorrect_listen_count(mock_server):
    mock_server.listen_count = 20

    cli = testutils.Cli(prepend_args=[
        '--verbosity', '3', 'listenbrainz-history', '--user=calliope_test'
    ])
    result = cli.run(['listens'])

    result.assert_success()
    listens = result.json()
    assert len(listens) == 100


def test_listens_since(mock_server):
    cli = testutils.Cli(prepend_args=[
        '--verbosity', '3', 'listenbrainz-history', '--user=calliope_test'
    ])

    playlist = cli.run(['artists', '--show-listens-since=2022-01-21 23:00:00']).json()
    assert len(playlist) == 4
    assert playlist[1]['creator'] == 'Obrint Pas'

    playlist = cli.run(['tracks', '--show-listens-since=2022-01-21 23:00:00']).json()
    assert len(playlist) == 5
    assert playlist[0]['creator'] == 'Victor Rice'
    assert playlist[0]['title'] == 'Time to Go'


def test_histogram(mock_server):
    cli = testutils.Cli(prepend_args=[
        '--verbosity', '3', 'listenbrainz-history', '--user=calliope_test'
    ])

    result = cli.run(['histogram', '--bucket=day'])
    result.assert_success()
    histogram = json.loads(result.stdout)
    assert histogram == [
        ['2022-01-17 00:00:00', 15],
        ['2022-01-18 00:00:00', 18],
        ['2022-01-19 00:00:00', 51],
        ['2022-01-21 00:00:00', 11],
        ['2022-01-22 00:00:00', 5],
    ]

    result = cli.run(['histogram', '--bucket=week'])
    result.assert_success()
    histogram = json.loads(result.stdout)
    assert histogram == [
        ['2022-01-23 00:00:00', 100]
    ]
