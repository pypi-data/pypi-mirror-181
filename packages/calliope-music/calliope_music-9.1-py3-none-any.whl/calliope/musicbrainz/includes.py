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


"""Helpers for filtering data when querying MusicBrainz."""


import dataclasses
from enum import Enum
import re


class MBType(Enum):
    """Supported MusicBrainz resource types."""
    ARTIST = 0
    RECORDING = 1
    RELEASE = 2
    RELEASE_GROUP = 4
    WORK = 4

    def typename(self) -> str:
        return self.name.lower().replace('_', '-')


ALL_MB_TYPES = {
    MBType.ARTIST, MBType.RECORDING, MBType.RELEASE, MBType.RELEASE_GROUP, MBType.WORK
}


@dataclasses.dataclass
class IncludeKey:
    """Include flags used in MusicBrainz API queries.

    Each MusicBrainz API call has an 'include' parameter to control what data
    is returned. This class represents each possible 'include' option.

    """

    # List of MusicBrainz resource types which take this key.
    types: set(MBType)

    # Key passed to 'include' in the relevant query function.
    name: str

    # Where data is found in the response.
    response_keys: [str]

    def applies_to_typename(self, typename) -> bool:
        type_enum = getattr(MBType, typename.upper().replace('-', '_'))
        return type_enum in self.types

    def fullnames(self) -> [str]:
        """List all fully qualified names of this key.

        A fullname is formatted as `typename.keyname`, for example:

          * artist.url-rels
          * recording.url-rels

        """
        return [f'{t.typename()}.{self.name}' for t in self.types]

    def outname(self) -> str:
        """Name used in Calliope Item keys.

        For example, 'artist-rels' becomes 'artist_rels'.

        """
        return self.name.replace('-', '_')

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)


# The include keys were taken from musicbrainzngs 0.7.1 docs:
# https://python-musicbrainzngs.readthedocs.io/en/v0.7.1/api/
#
# The list and count key names were found by manually inspecting
# the response from the server.
INCLUDE_KEYS = [
    IncludeKey(
        ALL_MB_TYPES,
        'aliases', ['alias-list']
    ),
    IncludeKey(
        ALL_MB_TYPES,
        'annotation', ['annotation-list']
    ),
    IncludeKey(
        ALL_MB_TYPES,
        'area-rels', ['area-relation-list']
    ),
    IncludeKey(
        {MBType.RECORDING, MBType.RELEASE_GROUP, MBType.RELEASE},
        'artist-credits', ['artist-credit', 'artist-credit-phrase']
    ),
    IncludeKey(
        ALL_MB_TYPES,
        'artist-rels', ['artist-relation-list']
    ),
    IncludeKey(
        {MBType.RECORDING, MBType.RELEASE_GROUP, MBType.RELEASE, MBType.WORK},
        'artists', ['artist-list']
    ),
    IncludeKey(
        {MBType.RECORDING, MBType.RELEASE_GROUP, MBType.RELEASE},
        'discids', ['discid-list']
    ),
    IncludeKey(
        ALL_MB_TYPES,
        'event-rels', ['event-relation-list']
    ),
    IncludeKey(
        ALL_MB_TYPES,
        'instrument-rels', ['instrument-relation-list']
    ),
    IncludeKey(
        {MBType.ARTIST, MBType.RECORDING, MBType.RELEASE},
        'isrcs', ['isrc-list']
    ),
    IncludeKey(
        ALL_MB_TYPES,
        'label-rels', ['label-relation-list']
    ),
    IncludeKey(
        {MBType.RELEASE},
        'labels', ['label-list']
    ),
    IncludeKey(
        {MBType.ARTIST, MBType.RECORDING, MBType.RELEASE_GROUP, MBType.RELEASE},
        'media', ['media-list']
    ),
    IncludeKey(
        ALL_MB_TYPES,
        'place-rels', ['place-relation-list']
    ),
    IncludeKey(
        {MBType.ARTIST, MBType.RECORDING, MBType.RELEASE_GROUP, MBType.WORK},
        'ratings', ['rating']
    ),
    IncludeKey(
        {MBType.RELEASE},
        'recording-level-rels', ['recording-level-relation-list']
    ),
    IncludeKey(
        ALL_MB_TYPES - {MBType.RECORDING},
        'recording-rels', ['recording-relation-list']
    ),
    IncludeKey(
        {MBType.ARTIST, MBType.RELEASE},
        'recordings', ['recording-list', 'recording-count']
    ),
    IncludeKey(
        ALL_MB_TYPES,
        'release-group-rels', ['release-group-relation-list']
    ),
    IncludeKey(
        {MBType.ARTIST, MBType.RELEASE},
        'release-groups', ['release-group-list']
    ),
    IncludeKey(
        ALL_MB_TYPES,
        'release-rels', ['release-relation-list']
    ),
    IncludeKey(
        {MBType.ARTIST, MBType.RECORDING, MBType.RELEASE_GROUP},
        'releases', ['release-list', 'release-count']
    ),
    IncludeKey(
        ALL_MB_TYPES,
        'series-rels', ['series-relation-list']
    ),
    IncludeKey(
        ALL_MB_TYPES,
        'tags', ['tag-list']
    ),
    IncludeKey(
        ALL_MB_TYPES,
        'url-rels', ['url-relation-list']
    ),
    IncludeKey(
        {MBType.RECORDING, MBType.RELEASE},
        'work-level-rels', ['work-level-relation-list']
    ),
    IncludeKey(
        ALL_MB_TYPES,
        'work-rels', ['work-relation-list']
    ),
    IncludeKey(
        {MBType.ARTIST},
        'works', ['work-list', 'work-count']
    ),

    # This key is a special case. The artist-credit field does not include
    # these keys, so they must be queried as extra data, however
    # get_artist_by_id() returns these keys in all cases. We gate them behind
    # this fake 'artist.base' include key.
    IncludeKey(
        {MBType.ARTIST},
        'base', ['area', 'begin-area', 'country', 'disambiguation',
                 'end_area', 'gender', 'ipis', 'isnis', 'life-span', 'type']
    ),
    # Not sure about this one.
    #'various-artists',
    # Avoid keys which require user authentication.
    # 'user-ratings', 'user-tags'
]


__key_fullname_map = None
def _key_fullname_map() -> [str,IncludeKey]:
    global __key_fullname_map  # pylint: disable=global-statement
    if __key_fullname_map is None:
        __key_fullname_map = {}
        for key in INCLUDE_KEYS:
            for fullname in key.fullnames():
                __key_fullname_map[fullname] = key
    return __key_fullname_map


def all_include_key_fullnames() -> set:
    return set(_key_fullname_map().keys())


def typenames() -> [str]:
    return [t.typename() for t in ALL_MB_TYPES]


def _pattern_to_re(pattern) -> re.Pattern:
    validate_re = re.compile('[^a-z-.*]')
    match = validate_re.search(pattern)
    if match:
        raise RuntimeError(
            f"Invalid character '{match.group(0)}' found in include pattern."
        )

    pattern_safe = pattern.replace('.', r'\.')
    code = '^' + pattern_safe.replace('*', '[a-z-.]+') + '$'
    return re.compile(code)


def get_key(fullname) -> IncludeKey:
    return _key_fullname_map()[fullname]


def expand_fullname_patterns(patterns: [str]) -> [str]:
    """Helper for tools which accept glob patterns for include-keys.

    This allows commandline users to specify "artist.*" rather than listing
    all artist include-keys explicitly.

    """
    result = set()

    def pattern_matchers():
        """Generate a match callback for each input pattern."""
        for pattern in patterns:
            # Python users often prefer _ over - as separator, so allow both.
            pattern = pattern.replace('_', '-')

            if '*' in pattern:
                pattern_re = _pattern_to_re(pattern)
                yield pattern_re.match
            else:
                yield pattern.__eq__

    matchers = list(pattern_matchers())
    for key in INCLUDE_KEYS:
        for fullname in key.fullnames():
            for matcher in matchers:
                if matcher(fullname):
                    result.add(fullname)

    return result
