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


import random
import pytest

pytest.importorskip("simpleai")


def test_duration(cli):
    def seconds(value):
        # Convert seconds to milliseconds for XSPF.
        return value * 1000

    playlist = [
        {'title': 'Track 1', 'creator': 'Artist 1', 'duration': seconds(30)},
        {'title': 'Track 2', 'creator': 'Artist 1', 'duration': seconds(60)},
        {'title': 'Track 3', 'creator': 'Artist 1', 'duration': seconds(90)},
        {'title': 'Track 4', 'creator': 'Artist 1', 'duration': seconds(120)},
        {'title': 'Track 5', 'creator': 'Artist 1', 'duration': seconds(150)},
        {'title': 'Track 1', 'creator': 'Artist 2', 'duration': seconds(180)},
        {'title': 'Track 2', 'creator': 'Artist 2', 'duration': seconds(210)},
        {'title': 'Track 3', 'creator': 'Artist 2', 'duration': seconds(240)},
        {'title': 'Track 4', 'creator': 'Artist 2', 'duration': seconds(270)},
        {'title': 'Track 5', 'creator': 'Artist 2', 'duration': seconds(300)},
    ]

    # List thats 10 minutes long.
    constraint_flags = [
        "--constraint=type:playlist-duration,vmin:10min,vmax:10min",
        "--constraint=type:item-duration,vmin:90sec,vmax:240sec",
    ]
    result = cli.run(['--verbosity', '3', 'select', '-'] + constraint_flags, input_playlist=playlist)
    result.assert_success()

    output = result.json()
    print(output)
    assert len(output) > 0

    # Give some flexibility on constraints.
    total_duration = sum(s['duration'] for s in output)
    assert seconds(500) < total_duration < seconds(700)
    assert not any(s['duration'] < seconds(60) for s in output)
    assert not any(s['duration'] > seconds(300) for s in output)


def test_genre_fraction_global(cli):
    playlist = [
        {'title': 'Track 1', 'creator': 'Artist 1', 'meta.tags': 'rock'},
        {'title': 'Track 2', 'creator': 'Artist 1', 'meta.tags': 'rap'},
        {'title': 'Track 3', 'creator': 'Artist 1', 'meta.tags': 'ska'},
        {'title': 'Track 4', 'creator': 'Artist 1', 'meta.tags': 'metal'},
        {'title': 'Track 5', 'creator': 'Artist 1', 'meta.tags': 'punk'},
        {'title': 'Track 1', 'creator': 'Artist 2', 'meta.tags': 'rock'},
        {'title': 'Track 2', 'creator': 'Artist 2', 'meta.tags': 'rap'},
        {'title': 'Track 3', 'creator': 'Artist 2', 'meta.tags': 'ska'},
        {'title': 'Track 4', 'creator': 'Artist 2', 'meta.tags': 'metal'},
        {'title': 'Track 5', 'creator': 'Artist 2', 'meta.tags': 'punk'},
    ]

    # List of 50% ska and 50% punk
    constraint_flags = [
        "--constraint=type:fraction-global;set,property:meta.tags,values:ska,fmin:0.5,fmax:0.5",
        "--constraint=type:fraction-global;set,property:meta.tags,values:punk,fmin:0.5,fmax:0.5",
    ]
    result = cli.run(['--verbosity', '3', 'select', '-'] + constraint_flags, input_playlist=playlist)
    result.assert_success()

    output = result.json()
    print(output)
    for track in output:
        assert track['meta.tags'] in ['ska', 'punk']
