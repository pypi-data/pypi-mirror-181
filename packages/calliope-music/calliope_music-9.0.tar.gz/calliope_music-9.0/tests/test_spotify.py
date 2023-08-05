import json
import os
import unittest.mock
from pathlib import Path
from typing import Dict
from unittest.mock import Mock

import pytest

import calliope
import testutils


def get_dummy_sp_search_paginated(responses):
    def dummy_search_paginated(
        api,
        query_str: str,
        item_type: str = "track",
        result_count_limit=300,
    ):
        json_path = Path(Path(__file__).parent, "data", responses[query_str])
        with open(json_path) as fd:
            return json.load(fd)

    return dummy_search_paginated


@pytest.fixture()
def mock_server(monkeypatch):
    def set_responses(responses):
        monkeypatch.setattr(
            calliope.spotify,
            "_search_paginated",
            get_dummy_sp_search_paginated(responses),
        )

    with unittest.mock.patch('calliope.spotify.SpotifyContext'):
        yield set_responses


class TestSpotifyCLI:
    @pytest.fixture()
    def cli(self):
        return testutils.Cli(prepend_args=["--verbosity=3", "spotify"])

    def assert_track_resolved(self, data, extra_fields=None):
        extra_fields = extra_fields or {}
        item = {
            "album": "Wonder Where We Land",
            "creator": "SBTRKT",
            "duration": 186436.0,
            "spotify.album": "Wonder Where We Land",
            "spotify.album_id": "4J9gt4YOazmavlYw4hMrfY",
            "spotify.artists": [
                {
                    'external_urls': {
                        'spotify': 'https://open.spotify.com/artist/1O10apSOoAPjOu6UhUNmeI'
                    },
                    'href': 'https://api.spotify.com/v1/artists/1O10apSOoAPjOu6UhUNmeI',
                    'id': '1O10apSOoAPjOu6UhUNmeI',
                    'name': 'SBTRKT',
                    'type': 'artist',
                    'uri': 'spotify:artist:1O10apSOoAPjOu6UhUNmeI'
                },
                {
                    'external_urls': {
                        'spotify': 'https://open.spotify.com/artist/4bS7w1U8P3Zuaa5jmj3mvN'
                    },
                    'href': 'https://api.spotify.com/v1/artists/4bS7w1U8P3Zuaa5jmj3mvN',
                    'id': '4bS7w1U8P3Zuaa5jmj3mvN',
                    'name': 'Denai Moore',
                    'type': 'artist',
                    'uri': 'spotify:artist:4bS7w1U8P3Zuaa5jmj3mvN'
                },
            ],
            "spotify.date": "2014-09-29",
            "spotify.duration_ms": 186436.0,
            "spotify.first_albumartist": "SBTRKT",
            "spotify.first_artist": "SBTRKT",
            "spotify.first_artist_id": "1O10apSOoAPjOu6UhUNmeI",
            "spotify.id": "1lFz7QPoxqBdUV4iugS3MX",
            "spotify.isrc": "GBBKS1400215",
            "spotify.popularity": 38,
            "spotify.title": "The Light",
            "title": "The Light",
        }
        item.update(extra_fields)
        assert data == [item]

    def test_resolve_track(self, cli, mock_server):
        mock_server(
            {
                "track:The Light artist:SBTRKT": "spotify.track:The Light artist:SBTRKT.json",
                "The Light SBTRKT": "spotify.The Light SBTRKT.json",
                "SBTRKT": "spotify.SBTRKT.json",
            }
        )

        playlist = [
            {
                "title": "The Light (feat. Denai Moore)",
                "creator": "SBTRKT",
                "album": "Wonder Where We Land",
            }
        ]

        result = cli.run(["resolve", "--update", "-"], input_playlist=playlist)
        result.assert_success()

        output = result.json()
        self.assert_track_resolved(output, extra_fields={
            'calliope.spotify.resolver_score': 0.977384780278671
        })

    def test_resolve_track_with_isrc(self, cli, mock_server):
        mock_server(
            {
                "isrc:GBBKS1400215": "spotify.isrc:GBBKS1400215.json",
                "track:The Light artist:SBTRKT": "spotify.track:The Light artist:SBTRKT.json",
                "The Light SBTRKT": "spotify.The Light SBTRKT.json",
                "SBTRKT": "spotify.SBTRKT.json",
            }
        )

        playlist = [
            {
                "title": "The Light (feat. Denai Moore)",
                "creator": "SBTRKT",
                "album": "Wonder Where We Land",
                "musicbrainz.isrcs": ["GBBKS1400215"],
            }
        ]

        result = cli.run(["resolve", "--update", "-"], input_playlist=playlist)
        result.assert_success()

        output = result.json()
        self.assert_track_resolved(output, extra_fields={
            'calliope.spotify.resolver_score': 0.9999929688533533,
            'musicbrainz.isrcs': ['GBBKS1400215'],
        })

    def test_resolve_track_with_id(self, cli, mock_server):
        mock_server(
            {
                "track:The Light artist:SBTRKT": "spotify.track:The Light artist:SBTRKT.json",
                "The Light SBTRKT": "spotify.The Light SBTRKT.json",
                "SBTRKT": "spotify.SBTRKT.json",
            }
        )

        playlist = [
            {
                "title": "The Light (feat. Denai Moore)",
                "creator": "SBTRKT",
                "album": "Wonder Where We Land",
                "spotify.id": "1lFz7QPoxqBdUV4iugS3MX",
            }
        ]

        result = cli.run(["resolve", "--update", "-"], input_playlist=playlist)
        result.assert_success()

        output = result.json()
        self.assert_track_resolved(output, extra_fields={
            'calliope.spotify.resolver_score': 0.9999929688533533
        })

    def test_resolve_track_with_artist_id(self, cli, mock_server):
        mock_server(
            {
                "track:The Light artist:SBTRKT": "spotify.track:The Light artist:SBTRKT.json",
                "The Light SBTRKT": "spotify.The Light SBTRKT.json",
                "SBTRKT": "spotify.SBTRKT.json",
            }
        )

        playlist = [
            {
                "title": "The Light (feat. Denai Moore)",
                "creator": "SBTRKT",
                "album": "Wonder Where We Land",
                "spotify.artists": [
                    { "id": "1O10apSOoAPjOu6UhUNmeI" },
                ],
            }
        ]

        result = cli.run(["resolve", "--update", "-"], input_playlist=playlist)
        result.assert_success()

        output = result.json()
        self.assert_track_resolved(output, extra_fields={
            'calliope.spotify.resolver_score': 0.977384780278671
        })

    def test_resolve_album(self, cli, mock_server):
        mock_server(
            {
                "artist:The Burning Hell album:Public Library": "spotify.artist:The Burning Hell album:Public Library.json",
                "The Burning Hell Public Library": "spotify.The Burning Hell Public Library.json",
                "The Burning Hell": "spotify.The Burning Hell.json",
            }
        )

        playlist = [
            {
                "album": "Public Library",
                "creator": "The Burning Hell",
            }
        ]

        result = cli.run(["resolve", "--update", "-"], input_playlist=playlist)
        result.assert_success()

        output = result.json()
        assert output == [
            {
                "album": "Public Library",
                "creator": "The Burning Hell",
                "spotify.album": "Public Library",
                "spotify.album_id": "36kt9AFzp9bueyRRBy6YmV",
                "spotify.albumartist": "The Burning Hell",
                "spotify.artist_id": "09kohMK0MSHgpmKWiQeQ5E",
                "spotify.date": "2016-04-01",
                "calliope.spotify.resolver_score": 0.9968340117593849,
            }
        ]


    def test_resolve_artist(self, cli, mock_server):
        mock_server(
            {
                "artist:Röyksopp": "spotify.artist:Röyksopp.json",
                "Röyksopp": "spotify.Röyksopp.json",
            }
        )

        playlist = [
            {
                "creator": "Röyksopp",
            }
        ]

        result = cli.run(["resolve", "--update", "-"], input_playlist=playlist)
        result.assert_success()

        output = result.json()
        assert output == [
            {
                "calliope.spotify.resolver_score": 1.0,
                "creator": "Röyksopp",
                "spotify.artist": "Röyksopp",
                "spotify.artist_id": "5nPOO9iTcrs9k6yFffPxjH",
            }
        ]


class TestSpotifyAPI:
    def test_export_library_track(self, capsys):
        def current_user_saved_tracks():
            json_path = Path(
                Path(__file__).parent, "data", "spotify_test_export_library_track_1.json"
            )
            with open(json_path) as fd:
                return json.load(fd)

        def next_(response):
            json_path = Path(
                Path(__file__).parent, "data", "spotify_test_export_library_track_2.json"
            )
            with open(json_path) as fd:
                return json.load(fd)

        context = Mock()
        context.api.current_user_saved_tracks = current_user_saved_tracks
        context.api.next = next_
        calliope.spotify.export_library_tracks(context)

        captured = capsys.readouterr()
        captured_str = "".join(captured.out)
        playlist = [json.loads(line) for line in captured_str.strip().split("\n")]
        assert playlist == [
            {
                "album": "Time Rider",
                "creator": "Chromatics",
                "duration": 283000.0,
                "playlist.title": "Spotify user library tracks",
                "spotify.album": "Time Rider",
                "spotify.album_id": "1lige5FVk5RvkVHZsuJ1eI",
                "spotify.artists": [
                    {
                        'external_urls': {
                            'spotify': 'https://open.spotify.com/artist/4tOVIRjlWWfR1RrAxyRqTE'
                        },
                        'href': 'https://api.spotify.com/v1/artists/4tOVIRjlWWfR1RrAxyRqTE',
                        'id': '4tOVIRjlWWfR1RrAxyRqTE',
                        'name': 'Chromatics',
                        'type': 'artist',
                        'uri': 'spotify:artist:4tOVIRjlWWfR1RrAxyRqTE'
                    }
                ],
                "spotify.date": "2019-02-19",
                "spotify.duration_ms": 283000.0,
                "spotify.first_albumartist": "Chromatics",
                "spotify.first_artist": "Chromatics",
                "spotify.first_artist_id": "4tOVIRjlWWfR1RrAxyRqTE",
                "spotify.id": "063P9fza0DJ5V4odLnVUcv",
                "spotify.isrc": "QM24S1907088",
                "spotify.popularity": 0,
                "spotify.title": "Time Rider",
                "title": "Time Rider",
            },
            {
                "album": "everything i wanted",
                "creator": "Billie Eilish",
                "duration": 245425.0,
                "spotify.album": "everything i wanted",
                "spotify.album_id": "4i3rAwPw7Ln2YrKDusaWyT",
                "spotify.artists": [
                    {
                        'external_urls': {
                            'spotify': 'https://open.spotify.com/artist/6qqNVTkY8uBg9cP3Jd7DAH'
                        },
                        'href': 'https://api.spotify.com/v1/artists/6qqNVTkY8uBg9cP3Jd7DAH',
                        'id': '6qqNVTkY8uBg9cP3Jd7DAH',
                        'name': 'Billie Eilish',
                        'type': 'artist',
                        'uri': 'spotify:artist:6qqNVTkY8uBg9cP3Jd7DAH'
                    }
                ],
                "spotify.date": "2019-11-13",
                "spotify.duration_ms": 245425.0,
                "spotify.first_albumartist": "Billie Eilish",
                "spotify.first_artist": "Billie Eilish",
                "spotify.first_artist_id": "6qqNVTkY8uBg9cP3Jd7DAH",
                "spotify.id": "3ZCTVFBt2Brf31RLEnCkWJ",
                "spotify.isrc": "USUM71922577",
                "spotify.popularity": 82,
                "spotify.title": "everything i wanted",
                "title": "everything i wanted",
            },
        ]


    def test_export_library_track_single(self, capsys):
        def current_user_saved_tracks():
            json_path = Path(
                Path(__file__).parent, "data", "spotify_test_export_library_track_1.json"
            )
            with open(json_path) as fd:
                data = json.load(fd)
            data["next"] = None
            return data

        context = Mock()
        context.api.current_user_saved_tracks = current_user_saved_tracks
        calliope.spotify.export_library_tracks(context)
        context.api.next.assert_not_called()

        captured = capsys.readouterr()
        captured_str = "".join(captured.out)
        playlist = [json.loads(line) for line in captured_str.strip().split("\n")]
        assert playlist == [
            {
                "album": "Time Rider",
                "creator": "Chromatics",
                "duration": 283000.0,
                "playlist.title": "Spotify user library tracks",
                "spotify.album": "Time Rider",
                "spotify.album_id": "1lige5FVk5RvkVHZsuJ1eI",
                "spotify.artists": [
                    {
                        'external_urls': {
                            'spotify': 'https://open.spotify.com/artist/4tOVIRjlWWfR1RrAxyRqTE'
                        },
                        'href': 'https://api.spotify.com/v1/artists/4tOVIRjlWWfR1RrAxyRqTE',
                        'id': '4tOVIRjlWWfR1RrAxyRqTE',
                        'name': 'Chromatics',
                        'type': 'artist',
                        'uri': 'spotify:artist:4tOVIRjlWWfR1RrAxyRqTE'
                    }
                ],
                "spotify.first_albumartist": "Chromatics",
                "spotify.first_artist": "Chromatics",
                "spotify.first_artist_id": "4tOVIRjlWWfR1RrAxyRqTE",
                "spotify.date": "2019-02-19",
                "spotify.duration_ms": 283000.0,
                "spotify.id": "063P9fza0DJ5V4odLnVUcv",
                "spotify.isrc": "QM24S1907088",
                "spotify.popularity": 0,
                "spotify.title": "Time Rider",
                "title": "Time Rider",
            }
        ]


    def test_export_library_track_none(self, capsys):
        def current_user_saved_tracks():
            json_path = Path(
                Path(__file__).parent, "data", "spotify_test_export_library_track_1.json"
            )
            with open(json_path) as fd:
                data = json.load(fd)
            data["items"] = []
            data["total"] = 0
            data["next"] = None

            return data

        context = Mock()
        context.api.current_user_saved_tracks = current_user_saved_tracks
        calliope.spotify.export_library_tracks(context)
        context.api.next.assert_not_called()

        captured = capsys.readouterr()
        captured_str = "".join(captured.out)
        assert captured_str == ""


    def test_export_library_album(self, capsys):
        def current_user_saved_albums():
            json_path = Path(
                Path(__file__).parent, "data", "spotify_test_export_library_album_1.json"
            )
            with open(json_path) as fd:
                data = json.load(fd)
            return data

        context = Mock()
        context.api.current_user_saved_albums = current_user_saved_albums
        calliope.spotify.export_library_albums(context)
        context.api.next.assert_not_called()

        captured = capsys.readouterr()
        captured_str = "".join(captured.out)
        playlist = [json.loads(line) for line in captured_str.strip().split("\n")]
        assert playlist == [
            {
                "album": "Wolves",
                "creator": "Digitalism",
                "playlist.title": "Spotify user library albums",
                "spotify.album": "Wolves",
                "spotify.album_id": "0HV9znyu4F3RUlNt4cW1y2",
                "spotify.albumartist": "Digitalism",
                "spotify.artist_id": "2fBURuq7FrlH6z5F92mpOl",
                "spotify.date": "2014-05-06",
            }
        ]


    def test_export_library_artist(self, capsys):
        def current_user_followed_artists():
            json_path = Path(
                Path(__file__).parent,
                "data",
                "spotify_current_user_followed_artists_1.json",
            )
            with open(json_path) as fd:
                data = json.load(fd)
            return data

        context = Mock()
        context.api.current_user_followed_artists = current_user_followed_artists
        calliope.spotify.export_library_artists(context)
        context.api.next.assert_not_called()

        captured = capsys.readouterr()
        captured_str = "".join(captured.out)
        playlist = [json.loads(line) for line in captured_str.strip().split("\n")]
        assert playlist == [
            {
                "creator": "Kadavar",
                "playlist.title": "Spotify user library artists",
                "spotify.artist": "Kadavar",
                "spotify.artist_id": "0FfuujZJUa7Z2JzhhiPI2z",
            }
        ]


    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ([1, 2, 3, 4, 5, 6], [[1, 2, 3], [4, 5, 6]]),
            ([1, 2, 3, 4, 5], [[1, 2, 3], [4, 5]]),
            ([1, 2, 3], [[1, 2, 3]]),
            ([1], [[1]]),
            ([], []),
        ],
    )
    def test__as_chunks(self, test_input, expected):
        result = list(calliope.spotify._as_chunks(test_input, 3))
        assert expected == result


    def test_import_library(self):

        context = Mock()

        playlist = [
            {"spotify.album_id": "album-id1"},
            {"spotify.album_id": "album-id2"},
            {"spotify.id": "id1"},
            {"spotify.id": "id2"},
            {"spotify.artist_id": "artist-id1"},
            {"spotify.artist_id": "artist-id2"},
            {"spotify.uri": "spotify:track:id3"},
            {"spotify.uri": "spotify:album:album-id3"},
            {"spotify.uri": "spotify:artist:artist-id3"},
        ]

        calliope.spotify.import_library(context, playlist)

        context.api.current_user_saved_tracks_add.assert_called_once_with(
            ["id1", "id2", "spotify:track:id3"]
        )
        context.api.current_user_saved_albums_add.assert_called_once_with(
            ["album-id1", "album-id2", "spotify:album:album-id3"]
        )
        context.api.user_follow_artists.assert_called_once_with(
            ["artist-id1", "artist-id2", "spotify:artist:artist-id3"]
        )


    def test_import_library_empty(self):

        context = Mock()

        calliope.spotify.import_library(context, [{"foo": "bar"}])

        context.api.current_user_saved_tracks_add.assert_not_called()
        context.api.current_user_saved_albums_add.assert_not_called()
        context.api.user_follow_artists.assert_not_called()


    def test_import_library_invalid_uri(self):

        context = Mock()

        calliope.spotify.import_library(context, [{"spotify.uri": "spotify:foobar:1234"}])

        context.api.current_user_saved_tracks_add.assert_not_called()
        context.api.current_user_saved_albums_add.assert_not_called()
        context.api.user_follow_artists.assert_not_called()
