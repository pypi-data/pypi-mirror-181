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

"""Data types used in calliope.spotify output."""


from calliope.playlist import Item as PlaylistItem


# This is not quite a playlist item, rather an extension
# of one. For now we subclass PlaylistItem as its basically
# a specialized dict() anyway.
class SpotifyArtistInfo(PlaylistItem):
    pass
