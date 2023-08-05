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


import pytest

import calliope

import testutils


def test_valid_playlist():
    playlist = [
        { 'title': 'Mesecina', 'creator': 'La Trocamba Matanusca',
          'custom.property': 'foo',
        }
    ]

    calliope.validate.validate(playlist)


def test_invalid_main_property():
    playlist = [
        { 'invalid-property': 'cheese' }
    ]

    with pytest.raises(calliope.validate.ValidationError):
        calliope.validate.validate(playlist)


@pytest.mark.parametrize("invalid_name", [
    'foo',
    '.foo',
    'foo.',
    'foo.bar.',
    '.foo.bar',
    'foo-bar',
])
def test_invalid_custom_property(invalid_name):
    with pytest.raises(calliope.validate.ValidationError):
        calliope.validate.validate([
            {invalid_name: 'cheese'}
        ])


@pytest.mark.parametrize("valid_name", [
    'foo.bar',
    'foo.bar.baz',
    'foo.bar_baz',
])
def test_invalid_custom_property(valid_name):
    calliope.validate.validate([
        {valid_name: 'cheese'}
    ])
