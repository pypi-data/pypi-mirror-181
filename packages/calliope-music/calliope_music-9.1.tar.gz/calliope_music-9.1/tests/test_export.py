# Calliope
# Copyright (C) 2018-2019  Sam Thursfield <sam@afuera.me.uk>
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


import json
import sys
import xml.etree.ElementTree

import pytest


def test_export_cue(cli):
    input_tracks = [
        { 'creator': 'Test1', 'play.start_time': 0 },
        { 'creator': 'Test2', 'play.start_time': 50 }
    ]

    expected_output = '\n'.join([
        "FILE \"none\" WAVE",
        "  TRACK 01 AUDIO",
        "    PERFORMER \"Test1\"",
        "  INDEX 01 00:00:00",
        "  TRACK 02 AUDIO",
        "    PERFORMER \"Test2\"",
        "  INDEX 01 00:50:00"])

    result = cli.run(['export', '--format=cue', '-'], input='\n'.join(json.dumps(track) for track in input_tracks))

    assert result.exit_code == 0
    assert result.stdout.strip() == expected_output


def test_export_m3u(cli):
    input_tracks = [
        { 'creator': 'Test1', 'location': 'file:///test1',
           'playlist.title': 'Test playlist' },
        { 'creator': 'Test2', 'location': 'file:///test2' }
    ]

    expected_output = '\n'.join([
        "#EXTM3U",
        "#PLAYLIST:Test playlist",
        "file:///test1",
        "file:///test2"
    ])

    result = cli.run(['export', '--format=m3u', '-'], input='\n'.join(json.dumps(track) for track in input_tracks))

    assert result.exit_code == 0
    assert result.stdout.strip() == expected_output


def test_export_jspf(cli):
    input_tracks = [
        { 'creator': 'Test1', 'location': 'file:///test1',
           'playlist.title': 'Test playlist' },
        { 'creator': 'Test2', 'location': 'file:///test2' }
    ]

    expected_output = """{
    "playlist": {
        "title": "expected_title",
        "track": [
            {
                "location": "file:///test1",
                "creator": "Test1"
            },
            {
                "location": "file:///test2",
                "creator": "Test2"
            }
        ]
    }
}"""

    result = cli.run(['export', '--format=jspf', '-'], input='\n'.join(json.dumps(track) for track in input_tracks))

    assert result.exit_code == 0
    assert result.stdout.strip() == expected_output.replace('expected_title', "Test playlist")

    result = cli.run(['export', '--format=jspf', '--title=Custom Title', '-'], input='\n'.join(json.dumps(track) for track in input_tracks))

    assert result.exit_code == 0
    assert result.stdout.strip() == expected_output.replace('expected_title', "Custom Title")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python >= 3.8")
def test_export_xspf(cli):
    input_tracks = [
        { 'creator': 'Test1', 'location': 'file:///test1',
           'playlist.title': 'Test playlist' },
        { 'creator': 'Test2', 'location': 'file:///test2' }
    ]

    expected_output = """<playlist xmlns="http://xspf.org/ns/0/" version="1">
	<title>expected_title</title>
	<trackList>
		<track>
			<location>file:///test1</location>
			<creator>Test1</creator>
		</track>
		<track>
			<location>file:///test2</location>
			<creator>Test2</creator>
		</track>
	</trackList>
</playlist>"""

    result = cli.run(['export', '--format=xspf', '-'], input='\n'.join(json.dumps(track) for track in input_tracks))

    assert result.exit_code == 0

    output = xml.etree.ElementTree.canonicalize(result.stdout.strip())
    assert output == expected_output.replace('expected_title', "Test playlist")

    result = cli.run(['export', '--format=xspf', '--title=Custom Title', '-'], input='\n'.join(json.dumps(track) for track in input_tracks))

    assert result.exit_code == 0

    output = xml.etree.ElementTree.canonicalize(result.stdout.strip())
    assert output == expected_output.replace('expected_title', "Custom Title")
