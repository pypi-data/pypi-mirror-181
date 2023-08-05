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


import calliope

def test_available_content_resolvers():
    result = calliope.available_content_resolvers()
    assert 'spotify' in result
    # This is not possible when we test inside a venv as we can't install `gi` there
    #assert 'tracker' in result


def test_available_listen_history_providers():
    result = calliope.available_listen_history_providers()
    assert 'lastfm_history' in result
    assert 'listenbrainz_history' in result
