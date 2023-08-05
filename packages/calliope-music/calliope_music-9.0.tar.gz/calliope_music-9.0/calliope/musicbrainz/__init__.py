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

"""Access data from `Musicbrainz <https://musicbrainz.org/>`_.

See also: :program:`cpe musicbrainz` command.

This module wraps the `musicbrainzngs <https://python-musicbrainzngs.readthedocs.io>`_ library.

Authentication
--------------

Musicbrainz access requires that you set a User Agent string. A default is set
by the :obj:`MusicbrainzContext` object which can be overridden using its
config.

Caching
-------

Caching of data is handled using the :mod:`calliope.cache` module.

"""

import logging
import warnings

import musicbrainzngs

import calliope.cache
import calliope.config
import calliope.playlist
from calliope.playlist import Item as PlaylistItem
from . import annotate_helpers, includes, resolve
from .context import MusicbrainzContext

log = logging.getLogger(__name__)


def _need_to_search(item: PlaylistItem) -> bool:
    search = False

    if 'title' in item:
        keys = ['musicbrainz.recording_id', 'musicbrainz.release_id',
                'musicbrainz.release_group_id', 'musicbrainz.work_id']
        for key in keys:
            if key not in item:
                search = True
    elif 'album' in item:
        keys = ['musicbrainz.release_id', 'musicbrainz.release_group_id']
        for key in keys:
            if key not in item:
                search = True
    elif 'creator' in item:
        if 'musicbrainz.artists' in item:
            for artist in item['musicbrainz.artists']:
                if 'id' not in artist:
                    search = True
        else:
            search = True
    else:
        warnings.warn("Did not find 'title', 'album' or 'creator' in item.")
    return search


def annotate(context: MusicbrainzContext,
             playlist: calliope.playlist.Playlist,
             include_patterns: [str],
             select_fun=None,
             update=False):
    """Annotate each item in a playlist with metadata from Musicbrainz.

    The ``include_patterns`` parameter controls what subqueries are run,
    via the MusicBrainz `include` query parameter.

    This parameter takes keys like `areas` or `url-rels` which cause more data
    to be fetched. MusicBrainz has different resource types, while in Calliope
    everything is a :class:`playlist item <calliope.playlist.Item>`, so within
    Calliope we specify keys as ``typename.key``. These are examples of
    different include key fullnames:

      * ``artist.areas``
      * ``artist.url-rels``
      * ``recording.url-rels``

    In ``include_patterns`` you can pass literal key names, and you can use
    ``*`` as a wildcard. For example, you can get all ``url-rels`` information
    with ``*.url-rels``, and all info about an artist with ``artist.*``.

    For reference documentation of the `include` parameter, see:
    <https://musicbrainz.org/doc/MusicBrainz_API#Subqueries>.

    Use :func:`calliope.includes.all_include_key_fullnames` to retrieve the
    full list of include keys.

    """

    if select_fun is None:
        select_fun = calliope.resolvers.select_best

    include = includes.expand_fullname_patterns(include_patterns)
    log.debug("include: %s", ','.join(include))

    for item in playlist:
        if _need_to_search(item):
            match = annotate_helpers.search(context, item, select_fun=select_fun)
            if match is not None:
                for key, v in match.items():
                    if key.startswith("musicbrainz.") or (update and "." not in key):
                        item[key] = v
                item["calliope.musicbrainz.resolver_score"] = match["_.priority"]

        item = annotate_helpers.query_data(context.cache, item, include)

        yield item


def resolve_image(context: MusicbrainzContext,
                  playlist: calliope.playlist.Playlist,
                  max_size: int=250):
    """Resolve a cover image using the Cover Art API.

    See https://musicbrainz.org/doc/Cover_Art_Archive/API for more info."""

    assert str(max_size) in ['250', '500', 'None']

    for item in playlist:
        if 'image' not in item:
            item = resolve.image_for_item(context, item, max_size)
        yield item
