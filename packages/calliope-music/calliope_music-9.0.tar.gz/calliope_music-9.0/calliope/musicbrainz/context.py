# Calliope
# Copyright (C) 2017-2021  Sam Thursfield <sam@afuera.me.uk>
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


import musicbrainzngs

import calliope.cache


class MusicbrainzContext():
    """Configuration for Musicbrainz APIs.

    Arguments:

      * ``app``: App name
      * ``version``: API version
      * ``contact``: Contact URL

    These are passed as the user agent to the musicbrainz API.
    """

    def __init__(self, app=None, version=None, contact=None):
        musicbrainzngs.set_useragent(app, version, contact)

        self.cache = calliope.cache.open(namespace='musicbrainz')
