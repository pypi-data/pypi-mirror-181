# Calliope
# Copyright (C) 2020  Sam Thursfield <sam@afuera.me.uk>
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


def fake_mp3(path):
    path.write_text("I'm an MP3 file, in theory.")
    return path.as_uri()


def fake_album(path):
    path.mkdir(exist_ok=True)
    for track in range(1,3):
        fake_mp3(path.joinpath(f"Track {track}.mp3"))
    return path.as_uri()


def test_copy_tracks(cli, tmp_path):
    sourcedir = tmp_path.joinpath('source')
    sourcedir.mkdir()
    targetdir = tmp_path.joinpath('target')
    targetdir.mkdir()

    playlist = [
        { 'location': fake_mp3(sourcedir.joinpath('a.mp3')) },
        { 'location': fake_mp3(sourcedir.joinpath('b.mp3')) },
    ]
    result = cli.run(['--verbosity', '3', 'sync', '--target', str(targetdir), '-'],
                     input_playlist=playlist)
    result.assert_success()

    assert targetdir.joinpath('a.mp3').exists()
    assert targetdir.joinpath('b.mp3').exists()


def test_copy_album_dirs(cli, tmp_path):
    sourcedir = tmp_path.joinpath('source')
    sourcedir.mkdir()
    targetdir = tmp_path.joinpath('target')
    targetdir.mkdir()

    playlist = [
        { 'location': fake_album(sourcedir.joinpath('Album 1')) },
        { 'location': fake_album(sourcedir.joinpath('Album 2')) },
    ]
    result = cli.run(['--verbosity', '3', 'sync', '--target', str(targetdir), '-'],
                     input_playlist=playlist)
    result.assert_success()

    assert targetdir.joinpath('Album 1/Track 1.mp3').exists()
    assert targetdir.joinpath('Album 1/Track 2.mp3').exists()
    assert targetdir.joinpath('Album 2/Track 1.mp3').exists()
    assert targetdir.joinpath('Album 2/Track 2.mp3').exists()
