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

'''Interface definitions for functionality that multiple modules can provide.

'''


from .playlist import Playlist


class ContentResolver:
    """Interface for modules that can resolve playable tracks."""

    def authenticate(self):
        raise NotImplementedError()

    def resolve_content(self, playlist: Playlist) -> Playlist:
        raise NotImplementedError()


class ListenHistoryProvider:
    """Interface for modules that provide a person's listening history."""

    def prepare_sync(self):
        raise NotImplementedError()

    def annotate(self, item):
        raise NotImplementedError()

    def scrobbles(self):
        raise NotImplementedError()

    def listens(self):
        raise NotImplementedError()

    def artists(self, first_play_before=None, first_play_since=None,
                last_play_before=None, last_play_since=None, min_listens=1,
                show_listens_since=None):
        raise NotImplementedError()

    def tracks(self, first_play_before=None, first_play_since=None,
               last_play_before=None, last_play_since=None, min_listens=1,
               show_listens_since=None):
        raise NotImplementedError()

    def histogram(self, bucket='year'):
        raise NotImplementedError()
