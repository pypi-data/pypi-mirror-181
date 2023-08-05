# Calliope
# Copyright (C) 2017-2021  Sam Thursfield <sam@afuera.me.uk>
# Copyright (C) 2021  Kilian Lackhove <kilian@lackhove.de>
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

import logging
from typing import Callable, Dict, List, Optional, Iterable
import warnings

import musicbrainzngs

from . import includes
from .schema import MusicBrainzArtistInfo
from calliope.playlist import Item
from calliope.resolvers import select_best
from calliope.utils import (
    drop_none_values,
    get_nested,
    normalize_creator_title,
    parse_sort_date,
)

log = logging.getLogger(__name__)


def _adapt_artist(mb_artist: Dict) -> MusicBrainzArtistInfo:
    return MusicBrainzArtistInfo(
        drop_none_values(
            {
                "area": mb_artist.get("area"),
                "begin_area": mb_artist.get("begin-area"),
                "country": mb_artist.get("country"),
                "disambiguation": mb_artist.get("disambiguation"),
                "end_area": mb_artist.get("end-area"),
                "gender": mb_artist.get("gender"),
                "id": mb_artist["id"],
                "ipis": mb_artist.get("ipis"),
                "isnis": mb_artist.get("isnis"),
                "life_span": mb_artist.get("life-span"),
                "name": mb_artist["name"],
                "sort_name": mb_artist.get("sort-name"),
                "type": mb_artist.get("type"),
            }
        )
    )

def _query_data_for_typename(cache, typename, mbid, include, query_cb) -> Dict:
    """
    Generic MusicBrainz query function

    Handles querying extra data for the following types: recording, release,
    release-group, work.
    """

    includes_to_query = set()
    data = {}

    def cache_key_for_include(keyname):
        return f'{mbid}.{typename}.{keyname}'

    for key in include:
        result = cache.lookup(cache_key_for_include(key.name))
        if result.found_timestamp is not None:
            data[key.name] = result.value
        else:
            includes_to_query.add(key)

    if len(includes_to_query) > 0:
        includes = list(
            key.name for key in includes_to_query
            if key.name != 'base'
        )
        log.debug("Calling %s: %s, %s", query_cb, mbid, includes)
        response = query_cb(mbid, includes=includes)
        response_data = response[typename]

        for key in includes_to_query:
            value = {}
            for response_key in key.response_keys:
                value[response_key] = response_data.get(response_key, [])
            cache.store(cache_key_for_include(key.name), value)
            data[key.name] = value

    return data


def query_data(cache, item, include: [str]) -> Item:
    """Query all MusicBrainz data specified by keys in ``include``."""

    def include_keys_for_type(typename):
        return [
            includes.get_key(fullname)
            for fullname in include
            if fullname.startswith(typename + '.')
        ]

    def attach_data_to_playlist_item(item, data, typename):
        for response_dict in data.values():
            for response_keyname, data_for_key in response_dict.items():
                out_keyname = response_keyname.replace('-', '_')

                prop = f'musicbrainz.{typename}.{out_keyname}'
                item[prop] = data_for_key
        return item

    artist_include_keys = include_keys_for_type('artist')
    if len(artist_include_keys) > 0:
        for i, artist in enumerate(item.get('musicbrainz.artists')):
            artist_mbid = artist.get('id')
            if artist_mbid:
                data = _query_data_for_typename(
                    cache, 'artist', artist_mbid, artist_include_keys,
                    musicbrainzngs.get_artist_by_id,
                )
                item['musicbrainz.artists'][i].update(data)

    recording_include_keys = include_keys_for_type('recording')
    if len(recording_include_keys) > 0:
        recording_mbid = item.get('musicbrainz.recording_id')
        if recording_mbid:
            data = _query_data_for_typename(
                cache, 'recording', recording_mbid, recording_include_keys,
                musicbrainzngs.get_recording_by_id,
            )
            item = attach_data_to_playlist_item(item, data, 'recording')

    release_include_keys = include_keys_for_type('release')
    if len(release_include_keys) > 0:
        release_mbid = item.get('musicbrainz.release_id')
        if release_mbid:
            data = _query_data_for_typename(
                cache, 'release', release_mbid, release_include_keys,
                musicbrainzngs.get_release_by_id,
            )
            item = attach_data_to_playlist_item(item, data, 'release')

    release_group_include_keys = include_keys_for_type('release-group')
    if len(release_group_include_keys) > 0:
        release_group_mbid = item.get('musicbrainz.release_group_id')
        if release_group_mbid:
            data = _query_data_for_typename(
                cache, 'release-group', release_group_mbid, release_group_include_keys,
                musicbrainzngs.get_release_group_by_id,
            )
            item = attach_data_to_playlist_item(item, data, 'release_group')

    work_include_keys = include_keys_for_type('work')
    if len(work_include_keys) > 0:
        work_mbid = item.get('musicbrainz.work_id')
        if work_mbid:
            data = _query_data_for_typename(
                cache, 'work', work_mbid, work_include_keys,
                musicbrainzngs.get_work_by_id,
            )
            item = attach_data_to_playlist_item(item, data, 'work')

    return item


def adapt_artist_credit(artist_credit: Iterable[Dict]) -> Iterable[Dict]:
    """
    Process 'artist-credit' field into a Calliope artist list.
    """

    musicbrainz_artists = []

    for credit in artist_credit:
        if isinstance(credit, dict):
            mb_artist_info = credit['artist']
            musicbrainz_artists.append(
                drop_none_values(
                    {
                        "country": mb_artist_info.get("country"),
                        "id": mb_artist_info["id"],
                        "name": mb_artist_info["name"],
                    }
                )
            )

    return musicbrainz_artists


def _recordings_to_items(mb_recordings: Iterable[Dict]) -> Iterable[Item]:
    """
    Convert musicbrainz recording dicts into calliope playlist items.

    The returned items can be passed into resolvers.py. Musicbrainz specific
    fields are prefixed with "musicbrainz." and fields that should not be visible
    to a user are prefixed with "_.". As many non-dotted fields are filled
    as possible.

    This produces one item for each release of each recording, so the number
    of returned items is higher than the number of input mb_recordings.

    Args:
        mb_recordings: An Iterable of musicbrainz recording dicts as returned by
            musicbrainzng.search_recording

    Returns:
        A calliope Item Iterator
    """

    for mb_recording in mb_recordings:
        mbreleases = mb_recording.get("release-list", [])
        if len(mbreleases) == 0:
            mbreleases.append(dict())
        for mb_release in mbreleases:

            item = Item(
                data={
                    "musicbrainz.title": mb_recording["title"],
                    "musicbrainz.album": mb_release.get("title"),
                    "musicbrainz.albumartist_credit": mb_release.get("artist-credit-phrase"),
                    "musicbrainz.artist_credit": mb_recording.get("artist-credit-phrase"),
                    "musicbrainz.artists": adapt_artist_credit(mb_recording.get("artist-credit")),
                    "musicbrainz.length": float(mb_recording["length"])
                    if "length" in mb_recording
                    else None,
                    "musicbrainz.release_id": mb_release.get("id"),
                    "musicbrainz.release_group_id": get_nested(
                        mb_release, ("release-group", "id")
                    ),
                    "musicbrainz.recording_id": mb_recording["id"],
                    "musicbrainz.date": mb_release.get("date"),
                    "musicbrainz.isrcs": mb_recording.get("isrc-list", None),
                    "_.secondary-type-list": get_nested(
                        mb_release, ("release-group", "secondary-type-list")
                    ),
                    "_.status": mb_release.get("status"),
                    "_.mb_score": mb_recording["ext:score"],
                    "_.release_count": len(mb_recording.get("release-list", [])),
                    "_.medium-track-count": get_nested(
                        mb_release, ("medium-list", 0, "track-count")
                    ),
                    "_.sort_date": parse_sort_date(mb_release.get("date")),
                }
            )

            for src, dst in (
                ("musicbrainz.title", "title"),
                ("musicbrainz.album", "album"),
                ("musicbrainz.artist_credit", "creator"),
                ("musicbrainz.length", "duration"),
                ("musicbrainz.albumartist_credit", "_.albumartist"),
                ("musicbrainz.date", "_.date"),
            ):
                item[dst] = item[src]

            yield drop_none_values(item)


def _releases_to_items(mb_releases: Iterable[Dict]) -> Iterable[Item]:
    """
    Convert musicbrainz release dicts into calliope playlist items.

    The returned items can be passed into resolvers.py. Musicbrainz specific
    fields are prefixed with "musicbrainz." and fields that should not be visible
    to a user are prefixed with "_.". As many non-dotted fields are filled
    as possible.

    Args:
        mb_releases: An Iterable of musicbrainz artist dicts as returned by
            musicbrainzng.search_release

    Returns:
        A calliope Item Iterator
    """

    for mb_release in mb_releases:

        item = Item(
            data={
                "musicbrainz.album": mb_release["title"],
                "musicbrainz.albumartist_credit": mb_release.get("artist-credit-phrase"),
                "musicbrainz.release_group_id": get_nested(
                    mb_release, ("release-group", "id")
                ),
                "musicbrainz.release_id": mb_release["id"],
                "musicbrainz.artists": adapt_artist_credit(mb_release["artist-credit"]),
                "musicbrainz.date": mb_release.get("date"),
                "_.secondary-type-list": get_nested(
                    mb_release, ("release-group", "secondary-type-list")
                ),
                "_.status": mb_release.get("status"),
                "_.sort_date": parse_sort_date(mb_release.get("date")),
            }
        )

        for src, dst in (
            ("musicbrainz.album", "album"),
            ("musicbrainz.albumartist_credit", "creator"),
            ("musicbrainz.albumartist_credit", "_.albumartist"),
            ("musicbrainz.date", "_.date"),
        ):
            item[dst] = item[src]

        yield drop_none_values(item)


def _artists_to_items(mb_artists: Iterable[Dict]) -> Iterable[Item]:
    """
    Convert musicbrainz artist dicts into calliope playlist items.

    The returned items can be passed into resolvers.py. Musicbrainz specific
    fields are prefixed with "musicbrainz." and fields that should not be visible
    to a user are prefixed with "_.". As many non-dotted fields are filled
    as possible.

    Args:
        mb_artists: An Iterable of musicbrainz artist dicts as returned by
            musicbrainzng.search_artist

    Returns:
        A calliope Item Iterator
    """

    for mb_artist in mb_artists:
        item = Item(
            data={
                "creator": mb_artist["name"],
                "musicbrainz.artists": [
                    _adapt_artist(mb_artist)
                ]
            }
        )

        yield drop_none_values(item)


def search(
    context,
    item: Item,
    select_fun: Callable[[Item, List[Item]], Optional[Item]] = select_best,
) -> Optional[Item]:
    """
    Search musicbrainz for the best match of item.

    Args:
        context: The musicbrainz context
        item: The item to search the match for
        select_fun: A selector function which chooses the best match from the
            retrieved candidates

    Returns:
        The match or None in case no good match was found.
    """

    query_kwargs = _build_search_kwargs(item)
    log.debug("Running search: %s", query_kwargs)
    if "title" in item:
        mb_recordings = context.cache.wrap(
            str(query_kwargs),
            lambda: _search_paginated(query_kwargs, musicbrainzngs.search_recordings),
        )
        candidates = _recordings_to_items(mb_recordings)
    elif "album" in item:
        mb_releases = context.cache.wrap(
            str(query_kwargs),
            lambda: _search_paginated(query_kwargs, musicbrainzngs.search_releases),
        )
        candidates = _releases_to_items(mb_releases)
    elif "creator" in item:
        mb_artists = context.cache.wrap(
            str(query_kwargs),
            lambda: _search_paginated(query_kwargs, musicbrainzngs.search_artists),
        )
        candidates = _artists_to_items(mb_artists)
    else:
        warnings.warn("Did not find 'title', 'album' or 'creator' in item.")
        return None

    candidates = list(candidates)
    if candidates is None or len(candidates) == 0:
        log.warning("Unable to find item on musicbrainz: {}".format(item))
        return None

    log.debug("Found {} candidates for item {}".format(len(candidates), repr(item)))
    match = select_fun(item, candidates)

    return match


def _build_search_kwargs(item: Item) -> Dict[str, str]:
    """
    Build and return musicbrainz search kwargs from an existing playlist item.

    Use the musicbrainz IDs where available or fall back to title/artist/album.
    This function can be used to build kwargs for searching for recordings,
    releases and artists.

    Args:
        item: An Item for which a musicbrainz match is sought

    Returns:
        A kwargs dict to pass into musicbrainzngs.search_*

    """

    recording_id = item.get("musicbrainz.recording_id")
    artist_id = item.get("musicbrainz.artist_id")
    release_id = item.get(
        "musicbrainz.release_id",
    )
    release_group_id = item.get("musicbrainz.release_group_id")

    title = item.get("title")
    creator = item.get("creator")
    creator, title = normalize_creator_title(creator, title)
    album = item.get("album")

    kwargs = dict()

    if recording_id is not None:
        kwargs["rid"] = recording_id
    elif title is not None:
        kwargs["recording"] = title

    if artist_id is not None:
        kwargs["arid"] = artist_id
    elif creator is not None:
        kwargs["artist"] = creator

    if release_id is not None:
        kwargs["reid"] = release_id
    if release_group_id is not None:
        kwargs["rgid"] = release_group_id

    # including the album name seems to cause musicbrainz to drop the best matches
    # in some cases, so this is disabled for recordings until we understand whats going on
    if (
        release_id is None
        and release_group_id is None
        and album is not None
        and title is None
    ):
        kwargs["release"] = album

    return kwargs


def _search_paginated(
    query_kwargs: Dict[str, str],
    search_func: Callable,
    result_score_limit=50,
    result_count_limit=300,
) -> List[Dict]:
    """
    Search musicbrainz using a specified search function and return as many
    results as RESULT_SCORE_LIMIT and RESULT_COUNT_LIMIT permit.

    Args:
        query_kwargs: A kwargs dict to pass into search_func
        search_func: A musicbrainzng.search_* function to call

    Returns:
        A list of dicts returned by search_func

    """
    elements = []
    offset = 0
    while True:
        response = search_func(**query_kwargs, limit=100, offset=offset)

        element_name = next(k.split("-")[0] for k in response if k.endswith("-list"))
        elements.extend(response[element_name + "-list"])
        if (
            len(elements) > result_count_limit
            or len(elements) == 0
            or int(elements[-1]["ext:score"]) < result_score_limit
            or len(elements) >= int(response[element_name + "-count"])
        ):
            break
        offset += 100

    return elements
