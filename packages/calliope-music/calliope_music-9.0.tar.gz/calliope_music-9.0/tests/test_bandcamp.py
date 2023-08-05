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


import pathlib


def test_export_album(cli):
    datadir = pathlib.Path(__file__).parent.joinpath('data')
    html_path = datadir.joinpath('bandcamp.album.html')
    result = cli.run(['bandcamp', 'export-album', html_path.as_uri()])

    album = result.json()
    assert album[0] == {
        'album': 'Mandatory Enjoyment',
        'bandcamp.album_id': 1199301027,
        'bandcamp.album_url': 'https://notdummy.bandcamp.com/album/mandatory-enjoyment',
        'bandcamp.artist_url': 'https://notdummy.bandcamp.com',
        'creator': 'Dummy',
        'duration': 93026,
        'location': 'https://notdummy.bandcamp.com/album/mandatory-enjoyment',
        'title': 'Protostar',
        'trackNum': 1
    }
    assert len(album) == 12


def test_export_band(cli):
    datadir = pathlib.Path(__file__).parent.joinpath('data')
    html_path = datadir.joinpath('bandcamp.band-label.html')
    result = cli.run(['bandcamp', 'export-band', html_path.as_uri()])

    albums = result.json()
    assert albums[0] == {
        'album': 'Roundelay',
        'bandcamp.album_id': '2916798840',
        'bandcamp.album_url': 'https://laketheband.bandcamp.com/album/roundelay?label=2157565508&tab=music',
        'bandcamp.artist_url': 'https://laketheband.bandcamp.com',
        'creator': 'LAKE',
        'location': 'https://laketheband.bandcamp.com/album/roundelay?label=2157565508&tab=music'
    }
    assert len(albums) == 13
