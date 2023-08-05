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


import calliope


def test_diff_empty():
    result = list(calliope.diff.diff([], []))
    assert len(result) == 0


def test_diff_simple():
    def make_item(index):
        return calliope.playlist.Item({
            "creator": f"Artist {index}",
            "title": f"Title {index}",
        })
    a = [
        make_item(0), make_item(1), make_item(2),
    ]
    b = [
        make_item(1), make_item(2), make_item(3),
    ]
    result = list(calliope.diff.diff(a, b))
    assert len(result) == 1
    assert result[0]['creator'] == 'Artist 0'


BANDCAMP_ALBUMS = [
    {"album": "Our Simulacra", "bandcamp.album_id": 1563537773, "creator": "The Flashbulb", "bandcamp.creator_id": "3639446620"},
    {"album": "Stay Evil", "bandcamp.album_id": 1795576787, "creator": "Black Ends", "bandcamp.creator_id": "749740660"},
    {"album": "SEVERED SEAS", "bandcamp.album_id": 1391287665, "creator": "AMULETS", "bandcamp.creator_id": "1290265776"},
    {"album": "Catbite", "bandcamp.album_id": 3203033784, "creator": "Catbite", "bandcamp.creator_id": "2270729651"},
]

BEETS_ALBUMS = [
    {"album": "Arboreal", "creator": "The Flashbulb",
        "musicbrainz.creator_id": "24786816-025f-49f4-9787-4945a3311f96",
        "musicbrainz.release_id": "6f0675eb-31db-4578-9235-6a7e8726d709",
        "musicbrainz.release_group_id": "ab207210-6cf5-4e3f-820c-9b462a3ecbba"},
    {"album": "Catbite", "creator": "Catbite",
        "musicbrainz.creator_id": "60721379-e2cb-4f6c-badf-a8874c069db5",
        "musicbrainz.release_id": "39d1ddf9-e967-4197-98c1-a2c37aa2cc5e",
        "musicbrainz.release_group_id": "c9885c12-1a5a-4348-91b6-3be0fcfd2b32"},
    {"album": "SEVERED SEAS", "creator": "AMULETS"},
    {"album": "\u5080\u5121\u96fb\u4f1d", "creator": "Dend\u00f6 Marionette",
        "musicbrainz.creator_id": "50844128-1bbe-47d2-93da-391a2fdd37a0",
        "musicbrainz.release_id": "850c553b-493a-4eeb-af40-f45115334913",
        "musicbrainz.release_group_id": "7f876ec1-fece-4c80-a235-684a97cd4085"},
]


def test_diff_creators_bandcamp_beets():
    gen = calliope.diff.diff(BANDCAMP_ALBUMS, BEETS_ALBUMS,
                             equal_function=calliope.diff.creator_equal)

    result = list(sorted(gen, key=lambda item: item['creator']))
    assert len(result) == 1
    print(result)
    assert result[0]['creator'] == 'Black Ends'


def test_diff_albums_bandcamp_beets():
    gen = calliope.diff.diff(BANDCAMP_ALBUMS, BEETS_ALBUMS,
                             equal_function=calliope.diff.album_equal)

    result = list(sorted(gen, key=lambda item: item['creator']))
    assert len(result) == 2
    print(result)
    assert result[0]['creator'] == 'Black Ends'
    assert result[1]['creator'] == 'The Flashbulb'
