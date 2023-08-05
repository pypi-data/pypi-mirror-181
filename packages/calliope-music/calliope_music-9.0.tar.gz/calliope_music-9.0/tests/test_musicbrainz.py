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


"""Tests for the `cpe musicbrainz` command."""

import io
import logging
import os
import re
import urllib.error
import urllib.parse
import urllib.request

import pytest

musicbrainzngs = pytest.importorskip("musicbrainzngs")
import testutils


# Pretend to be a musicbrainz server.
#
# Adapted from here:
# https://github.com/alastair/python-musicbrainzngs/blob/master/test/_common.py
class FakeOpener(urllib.request.OpenerDirector):
    """Fake URL opener for providing a mock Musicbrainz server."""

    def __init__(self, response_set):
        self.myurl = None
        self.headers = None
        self.response_set = response_set

    def open(self, request, body=None):
        self.myurl = request.get_full_url()
        self.headers = request.header_items()
        self.request = request

        return self.response_set.open(request.get_full_url())

    def get_url(self):
        return self.myurl


class ResponseSet:
    """A table of responses for the fake server to provide.

    The response_table should be a list of tuples, where each tuple maps a
    regular expression, matched against the URL path and query, to a response.
    The response should be a string to be returned, or an Exception subclass
    to be raised.

    """

    def __init__(self, response_table):
        self.response_table = response_table
        self.log = logging.getLogger("mock musicbrainz server")

    def open(self, url):
        to_match = url

        for pattern, response in self.response_table:
            if pattern == to_match or re.match(pattern, to_match):
                self.log.debug("Matched URL %s against %s", url, pattern)
                if isinstance(response, Exception):
                    raise response
                return io.BytesIO(response.encode("utf-8"))
        else:
            self.log.warning("No URL patterns matched %s, returning 404", url)
            return urllib.error.HTTPError("", 404, "", "", io.StringIO(""))


def stock_response(filename):
    """Return a pre-downloaded Musicbrainz response from the data/ subdir."""
    data_path = os.path.join(os.path.dirname(__file__), "data", filename)
    with open(data_path) as f:
        return f.read()


def error_404():
    return urllib.error.HTTPError("", 404, "", "", io.StringIO(""))


@pytest.fixture()
def mock_server(monkeypatch):
    def set_responses(responses):
        monkeypatch.setattr(
            "musicbrainzngs.compat.build_opener",
            lambda *args: FakeOpener(ResponseSet(responses)),
        )

    return set_responses


@pytest.fixture()
def cli():
    return testutils.Cli(prepend_args=["--verbosity", "3", "musicbrainz"])


MB = r"https://musicbrainz.org/ws/2"
COVERART = r"https://coverartarchive.org"


def test_list_includes(cli):
    result = cli.run(["list-includes"])
    result.assert_success()


class TestArtists():
    def assert_artist_resolved(self, data, extra_fields=None,
                               extra_first_artist_info=None):
        expected = {
            "creator": "Röyksopp",
            "musicbrainz.artists": [
                {
                    "area": {"id": "6743d351-6f37-3049-9724-5041161fff4d",
                             "life-span": {"ended": "false"},
                             "name": "Norway",
                             "sort-name": "Norway",
                             "type": "Country"},
                    "begin_area": {"id": "8bd9b44c-3b6c-4652-b830-204797952f41",
                                   "life-span": {"ended": "false"},
                                   "name": "Tromsø",
                                   "sort-name": "Tromsø",
                                   "type": "Municipality"},
                    "country": "NO",
                    "id": "1c70a3fc-fa3c-4be1-8b55-c3192db8a884",
                    "life_span": {"begin": "1998",
                                  "ended": "false"},
                    "name": "Röyksopp",
                    "sort_name": "Röyksopp",
                    "type": "Group",
                }
            ]
        }
        expected.update(extra_fields or {})
        expected['musicbrainz.artists'][0].update(extra_first_artist_info or {})
        assert data == [expected]

    def test_resolve_artist(self, cli, mock_server):
        mock_server(
            [
                (
                    MB + r"/artist/\?limit=100&query=artist%3A%28r%C3%B6yksopp%29",
                    stock_response("musicbrainz-search-artist.xml"),
                ),
            ]
        )

        playlist = [{"creator": "Röyksopp"}]

        result = cli.run(["annotate", "--output", "-", "-"], input_playlist=playlist)
        result.assert_success()

        output = result.json()
        self.assert_artist_resolved(output, extra_fields= {
            "calliope.musicbrainz.resolver_score": 1.0,
        })

    def test_annotate_artists(self, cli, mock_server):
        mock_server(
            [
                (
                    MB + r"/artist/\?limit=100&query=artist%3A%28r%C3%B6yksopp%29",
                    stock_response("musicbrainz-search-artist.xml"),
                ),
                (
                    MB + r"/artist/1c70a3fc-fa3c-4be1-8b55-c3192db8a884?inc=aliases",
                    stock_response("musicbrainz.annotate_artist_aliases.xml"),
                ),
            ]
        )

        playlist = [{"creator": "Röyksopp"}]

        result = cli.run(["annotate", "--include", "artist.aliases", "--output", "-", "-"], input_playlist=playlist)
        result.assert_success()

        output = result.json()
        self.assert_artist_resolved(
            output,
            extra_fields={
                "calliope.musicbrainz.resolver_score": 1.0,
            },
            extra_first_artist_info={
                'aliases': {
                    'alias-list': [
                        {'alias': 'RYXP', 'sort-name': 'RYXP', 'type': 'Artist name'},
                        {'alias': 'Roksopp', 'sort-name': 'Roksopp', 'type': 'Search hint'},
                        {'alias': 'Royksopp', 'sort-name': 'Royksopp', 'type': 'Search hint'},
                        {'alias': 'Royskopp', 'sort-name': 'Royskopp', 'type': 'Search hint'},
                        {'alias': 'Ryksopp', 'sort-name': 'Ryksopp', 'type': 'Search hint'},
                        {'alias': 'Röyksoop', 'sort-name': 'Röyksoop', 'type': 'Search hint'},
                        {'alias': 'Røyksopp', 'sort-name': 'Røyksopp'}
                    ]
                }
            }
        )


def test_resolve_album(cli, mock_server):
    mock_server(
        [
            (
                MB
                + "/release/?limit=100&query=artist%3A%28the+burning+hell%29+release%3A%28public+library%29",
                stock_response("musicbrainz.resolve_album.xml"),
            ),
        ]
    )

    playlist = [
        {
            "album": "Public Library",
            "creator": "The Burning Hell",
        }
    ]

    result = cli.run(["annotate", "--output", "-", "-"], input_playlist=playlist)
    result.assert_success()

    output = result.json()
    assert output == [
        {
            "album": "Public Library",
            "creator": "The Burning Hell",
            "musicbrainz.album": "Public Library",
            "musicbrainz.albumartist_credit": "The Burning Hell",
            "musicbrainz.artists": [
                {
                    "id": "4d55b744-b94d-44ef-bc99-15cd1cbe3cca",
                    "name": "The Burning Hell",
                }
            ],
            "musicbrainz.date": "2016-04-01",
            "musicbrainz.release_group_id": "466da3b9-a5a7-42ea-ab03-bdcaa64f41bd",
            "musicbrainz.release_id": "b8f7019c-a57d-4bd2-840a-b3ea80bcd32c",
            "calliope.musicbrainz.resolver_score": 0.9975124378109452,
        }
    ]


def test_resolve_invalid(cli, mock_server):
    mock_server([(".*", error_404())])

    playlist = [{"nonsense": "nothing"}]

    with pytest.warns(UserWarning):
        result = cli.run(["annotate", "--output", "-", "-"], input_playlist=playlist)
    result.assert_success()


class TestRecordings():
    def test_resolve_track(self, cli, mock_server):
        mock_server(
            [
                (
                    MB
                    + r"/recording/\?limit=100&query=recording.*the\+light.*\+artist.*sbtrkt\+denai\+moore.*",
                    stock_response("musicbrainz.search-recording.xml"),
                ),
            ]
        )

        playlist = [
            {
                "title": "The Light feat. Denai Moore",
                "creator": "SBTRKT",
                "album": "Wonder Where We Land",
                "duration": 186.408,
            }
        ]

        result = cli.run(
            ["annotate", "--update", "--output", "-", "-"], input_playlist=playlist
        )
        result.assert_success()

        output = result.json()
        assert output == [
            {
                "album": "Wonder Where We Land",
                "creator": "SBTRKT feat. Denai Moore",
                "duration": 186436.0,
                "musicbrainz.album": "Wonder Where We Land",
                "musicbrainz.albumartist_credit": "SBTRKT",
                "musicbrainz.artist_credit": "SBTRKT feat. Denai Moore",
                "musicbrainz.artists": [
                    {
                        "id": "7f2aa196-cfd4-4a3d-ace3-28b7b6a79af7",
                        "name": "SBTRKT"
                    },
                    {
                        "id": "b10391f5-c730-4ad9-a099-fab47843fe97",
                        "name": "Denai Moore"
                    },
                ],
                "musicbrainz.date": "2014-09-24",
                "musicbrainz.isrcs": ["GBBKS1400215"],
                "musicbrainz.length": 186436.0,
                "musicbrainz.recording_id": "13b18d21-9600-419c-888e-99c9c5e1d9a3",
                "musicbrainz.release_id": "59c00320-db1c-4f45-b8ff-889281b544a1",
                "musicbrainz.release_group_id": "08c5a214-0628-4257-837d-f6e56a043631",
                "musicbrainz.title": "The Light",
                "title": "The Light",
                "calliope.musicbrainz.resolver_score": 0.9945150019690607,
            }
        ]

    def test_resolve_track_artist_base_info(self, cli, mock_server):
        """Test the special artist.base include key."""
        mock_server(
            [
                (
                    MB
                    + r"/recording/\?limit=100&query=recording.*the\+light.*\+artist.*sbtrkt\+denai\+moore.*",
                    stock_response("musicbrainz.search-recording.xml"),
                ),
                (
                    MB + r"/artist/7f2aa196-cfd4-4a3d-ace3-28b7b6a79af7",
                    stock_response("musicbrainz.artist.sbtrkt.xml"),
                ),
                (
                    MB + r"/artist/b10391f5-c730-4ad9-a099-fab47843fe97",
                    stock_response("musicbrainz.artist.denai_moore.xml"),
                ),
            ]
        )

        playlist = [
            {
                "title": "The Light feat. Denai Moore",
                "creator": "SBTRKT",
                "album": "Wonder Where We Land",
                "duration": 186.408,
            }
        ]

        result = cli.run(
            ["annotate", "--update", "--include=artist.base", "--output", "-", "-"], input_playlist=playlist
        )
        result.assert_success()

        output = result.json()
        assert output == [
            {
                "album": "Wonder Where We Land",
                "creator": "SBTRKT feat. Denai Moore",
                "duration": 186436.0,
                "musicbrainz.album": "Wonder Where We Land",
                "musicbrainz.albumartist_credit": "SBTRKT",
                "musicbrainz.artist_credit": "SBTRKT feat. Denai Moore",
                "musicbrainz.artists": [
                    {
                        "id": "7f2aa196-cfd4-4a3d-ace3-28b7b6a79af7",
                        "name": "SBTRKT",
                        "base": {
                            'area': {
                                'id': '8a754a16-0027-3a29-b6d7-2b40ea0481ed',
                                'iso-3166-1-code-list': ['GB'],
                                'name': 'United Kingdom',
                                'sort-name': 'United Kingdom'
                            },
                            'begin-area': {
                                'disambiguation': 'Greater London, which includes the City of London',
                                'id': 'f03d09b3-39dc-4083-afd6-159e3f0d462f',
                                'name': 'London',
                                'sort-name': 'London'
                            },
                            'country': 'GB',
                            'disambiguation': [],
                            'end_area': [],
                            'gender': 'Male',
                            'ipis': [],
                            'isnis': [],
                            'life-span': [],
                            'type': 'Person',
                        }
                    },
                    {
                        "id": "b10391f5-c730-4ad9-a099-fab47843fe97",
                        "name": "Denai Moore",
                        "base": {
                            'area': {
                                'disambiguation': 'Greater London, which includes the City of London',
                                'id': 'f03d09b3-39dc-4083-afd6-159e3f0d462f',
                                'name': 'London',
                                'sort-name': 'London'
                            },
                            'begin-area': [],
                            'country': [],
                            'disambiguation': [],
                            'end_area': [],
                            'gender': 'Female',
                            'ipis': [],
                            'isnis': [],
                            'life-span': [],
                            'type': 'Person',
                        }
                    },
                ],
                "musicbrainz.date": "2014-09-24",
                "musicbrainz.isrcs": ["GBBKS1400215"],
                "musicbrainz.length": 186436.0,
                "musicbrainz.recording_id": "13b18d21-9600-419c-888e-99c9c5e1d9a3",
                "musicbrainz.release_id": "59c00320-db1c-4f45-b8ff-889281b544a1",
                "musicbrainz.release_group_id": "08c5a214-0628-4257-837d-f6e56a043631",
                "musicbrainz.title": "The Light",
                "title": "The Light",
                "calliope.musicbrainz.resolver_score": 0.9945150019690607,
            }
        ]

    def test_resolve_track_with_isrc(self, cli, mock_server):
        mock_server(
            [
                (
                    MB
                    + r"/recording/\?limit=100&query=recording%3A%28like\+eating\+glass%29\+artist%3A%28bloc\+party%29",
                    stock_response("musicbrainz.resolve_track_with_isrc.xml"),
                ),
            ]
        )

        playlist = [
            {
                "title": "Like Eating Glass",
                "creator": "Bloc Party",
                "musicbrainz.isrcs": ["QM6MZ1916107"],
            }
        ]

        result = cli.run(["annotate", "--output", "-", "-"], input_playlist=playlist)
        result.assert_success()

        output = result.json()[0]

        assert output["musicbrainz.album"] == "Silent Alarm Live"
        assert output["musicbrainz.artists"][0]["id"] == "8c538f11-c141-4588-8ecb-931083524186"
        assert output["musicbrainz.isrcs"] == ["QM6MZ1916107"]
        assert output["musicbrainz.recording_id"] == "5667663d-a5f9-46cd-868b-ab8822e4f3ee"
        assert (
            output["musicbrainz.release_group_id"] == "274009ee-3e4d-476c-9a79-eed4d81efebb"
        )


    def test_resolve_track_with_rid(self, cli, mock_server):
        mock_server(
            [
                (
                    MB
                    + r"/recording/?limit=100&query=rid%3A%285667663d%5C-a5f9%5C-46cd%5C-868b%5C-ab8822e4f3ee%29",
                    stock_response("musicbrainz.resolve_track_with_rid.xml"),
                ),
            ]
        )

        playlist = [
            {
                "title": "foo",
                "musicbrainz.recording_id": "5667663d-a5f9-46cd-868b-ab8822e4f3ee",
            }
        ]

        result = cli.run(["annotate", "-"], input_playlist=playlist)
        result.assert_success()

        output = result.json()[0]

        assert output["musicbrainz.album"] == "Silent Alarm Live"
        assert output["musicbrainz.artists"][0]["id"] == "8c538f11-c141-4588-8ecb-931083524186"
        assert output["musicbrainz.recording_id"] == "5667663d-a5f9-46cd-868b-ab8822e4f3ee"
        assert (
            output["musicbrainz.release_group_id"] == "274009ee-3e4d-476c-9a79-eed4d81efebb"
        )


    def test_resolve_track_with_rgid(self, cli, mock_server):
        mock_server(
            [
                (
                    MB
                    + r"/recording/?limit=100&query=recording%3A%28like+eating+glass%29+rgid%3A%28274009ee%5C-3e4d%5C-476c%5C-9a79%5C-eed4d81efebb%29",
                    stock_response("musicbrainz.resolve_track_with_rgid.xml"),
                ),
            ]
        )

        playlist = [
            {
                "title": "Like Eating Glass",
                "musicbrainz.release_group_id": "274009ee-3e4d-476c-9a79-eed4d81efebb",
            }
        ]

        result = cli.run(["annotate", "--output", "-", "-"], input_playlist=playlist)
        result.assert_success()

        output = result.json()[0]

        assert output["musicbrainz.album"] == "Silent Alarm Live"
        assert output["musicbrainz.artists"][0]["id"] == "8c538f11-c141-4588-8ecb-931083524186"
        assert output["musicbrainz.recording_id"] == "5667663d-a5f9-46cd-868b-ab8822e4f3ee"
        assert (
            output["musicbrainz.release_group_id"] == "274009ee-3e4d-476c-9a79-eed4d81efebb"
        )


def test_resolve_image(cli, mock_server):
    mock_server(
        [
            (
                MB + r"/release/\?query=Richard\+AND\+Dawson\+AND\+2020",
                stock_response("musicbrainz-search-release.richard-dawson-2020.xml"),
            ),
            (
                COVERART + r"/release/2757d45c-3404-41db-92c2-a82a76d70363",
                stock_response("coverartarchive-release.richard-dawson-2020.xml"),
            ),
        ]
    )

    playlist = [{"creator": "Richard Dawson", "album": "2020"}]

    result = cli.run(["resolve-image", "-"], input_playlist=playlist)
    result.assert_success()

    output = result.json()
    assert output == [
        {
            "creator": "Richard Dawson",
            "album": "2020",
            "musicbrainz.artists": [
                {
                    "id": "ee7923b9-5850-47b5-97cc-5cecdc21578d",
                    "name": "Richard Dawson",
                },
            ],
            "musicbrainz.release_id": "2757d45c-3404-41db-92c2-a82a76d70363",
            "musicbrainz.release_group_id": "feb16471-6a08-4ded-9b46-c9b76e8d90a2",
            "image": "http://coverartarchive.org/release/2757d45c-3404-41db-92c2-a82a76d70363/24066950835-250.jpg",
        }
    ]


def test_releases_invalid_album_mbid(cli, mock_server):
    """The playlist may specify an MBID that's incorrect."""

    playlist = [
        {
            "creator": "Alvvays",
            "album": "Alvvays",
            "title": "Atop a Cake",
            "musicbrainz.artists": [
                { "id": "99450990-b24e-4132-bb68-235f8c3e2564" },

            ],
            "musicbrainz.album_id": "0ea1ee01-54b6-439f-bf01-250375741813",
            "musicbrainz.identifier": "5d571740-6d0c-40d7-96fe-91391dbc91f5",
        }
    ]

    mock_server(
        [
            (MB + r"/release/0ea1ee01-54b6-439f-bf01-250375741813", error_404()),
        ]
    )

    result = cli.run(["annotate", "--include=release", "-"], input_playlist=playlist)
    assert isinstance(result.exception, musicbrainzngs.ResponseError)


def test_server_error(cli, mock_server):
    """Inject a 404 error and see how the client responds.

    For simplicity, the client doesn't handle these exceptions currently so
    we test for an unhandled musicbrainzngs.ResponseError().

    """
    mock_server([(".*", error_404())])

    playlist = [
        {
            "title": "The Light feat. Denai Moore",
            "creator": "SBTRKT",
            "album": "Wonder Where We Land",
            "duration": 186.408,
        }
    ]

    result = cli.run(["annotate", "-"], input_playlist=playlist)

    assert isinstance(result.exception, musicbrainzngs.ResponseError)
