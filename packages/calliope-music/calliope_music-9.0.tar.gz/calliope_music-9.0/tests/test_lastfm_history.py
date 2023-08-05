# Calliope
# Copyright (C) 2019  Sam Thursfield <sam@afuera.me.uk>
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


"""Tests for the `cpe lastfm-history` command."""


import pytest

pytest.importorskip("calliope.subprojects.lastfmclient")

import json
import logging
import os
import sys
import urllib.parse
import wsgiref.util

import testutils


@pytest.fixture()
def server():
    '''Pretend to be a Last.fm / Libre.fm server.'''

    template_path = os.path.join(os.path.dirname(__file__), 'data', 'lastfm-history.xml')

    def handle_request(environ, start_response):
        wsgiref.util.setup_testing_defaults(environ)

        params = urllib.parse.parse_qs(environ['QUERY_STRING'])
        method = params['method'][0]
        page = params['page'][0]
        user = params['user'][0]
        api_key = params['api_key'][0]

        logging.debug("Test server: Got request with params: %s", params)

        if method == 'user.getrecenttracks' and page == '1':
            assert api_key == 'lastexport.py-0.0.4-------------'
            assert user == 'calliope_test'
            status = '200 OK'
            headers = [('Content-type', 'text/xml; charset=utf-8')]
            start_response(status, headers)
            return wsgiref.util.FileWrapper(open(template_path, 'rb'))
        else:
            status = '404 NOT FOUND (method: %s)' % (method)
            start_response(status, [('Content-type', 'text/plain')])
            return [b'not found']

    server = testutils.MockWebServer(handle_request)
    server.start()
    return server.base_uri()


def test_basic(server):
    cli = testutils.Cli(prepend_args=['--verbosity', '3', 'lastfm-history', '--user=calliope_test', '--server=%s' % server, '--no-retry-on-error'])
    result = cli.run(['listens'])
    result.assert_success()
    listens = result.json()
    assert len(listens) == 50
    assert listens[0]['creator'] == 'Ye Nuns'


def test_listens_since(server):
    cli = testutils.Cli(prepend_args=['--verbosity', '3', 'lastfm-history', '--user=calliope_test', '--server=%s' % server, '--no-retry-on-error'])

    playlist = cli.run(['artists', '--min-listens=2', '--show-listens-since=2019-11-18']).json()
    assert len(playlist) == 4
    assert playlist[1]['creator'] == 'The Fiery Furnaces'
    assert playlist[1]['lastfm.playcount'] == 3
    assert playlist[1]['lastfm.listens_since_2019_11_18'] == 1

    playlist = cli.run(['tracks', '--min-listens=2', '--show-listens-since=2019-11-18']).json()
    assert len(playlist) == 1
    assert playlist[0]['creator'] == 'The Fiery Furnaces'
    assert playlist[0]['title'] == 'Nevers'
    assert playlist[0]['lastfm.playcount'] == 2
    assert playlist[0]['lastfm.listens_since_2019_11_18'] == 1


def test_histogram(server):
    cli = testutils.Cli(prepend_args=[
        '--verbosity', '3', 'lastfm-history', '--user=calliope_test', '--server=%s' % server, '--no-retry-on-error'
    ])

    result = cli.run(['histogram', '--bucket=day'])
    result.assert_success()
    histogram = json.loads(result.stdout)
    assert histogram == [
        ['2019-11-17 00:00:00', 31],
        ['2019-11-18 00:00:00', 1],
        ['2019-11-19 00:00:00', 16],
        ['2019-11-20 00:00:00', 2],
    ]

    result = cli.run(['histogram', '--bucket=week'])
    result.assert_success()
    histogram = json.loads(result.stdout)
    assert histogram == [
        ['2019-11-17 00:00:00', 31],
        ['2019-11-24 00:00:00', 19],
    ]
