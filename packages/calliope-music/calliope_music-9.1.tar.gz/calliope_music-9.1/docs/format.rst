Playlist format
===============

Overview
--------

The Calliope playlist format is very similar to `XSPF
<http://www.xspf.org/>`_. For a list of available properties and their
meanings, see the `XSPF specification
<http://www.xspf.org/xspf-v1.html#rfc.section.4.1.1.2.14.1>`_.

The XSPF format is not suited to line-based processing, so the Calliope
playlist format has some differences from XSPF:

 1. A playlist is a `JSON Lines <http://jsonlines.org/>`_ stream,
    and playlist item is a separate JSON document.

 2. In addition to the properties defined by XSPF, a playlist may contain
    any number of *custom properties*. These must be namespaced using a `.`
    character. For example ``creator`` is an *XSPF property*, while
    ``musicbrainz.artist_id`` is a *custom property* in the 'musicbrainz'
    namespace.

Working with the Calliope playlist format
-----------------------------------------

The ``cpe validate`` command can validate that a playlist stream
conforms to the schema.

The ``cpe import`` and ``cpe export`` commands convert between the
Calliope playlist format and other formats. It's recommended that
you store your playlists on disk in XSPF format, so other applications can read
them, and use the ``cpe import`` and ``cpe export`` commands when you want to
bring them in and out of Calliope operations.

Example playlist
----------------

Here is a short example of a Calliope format playlist.
Remember that the format is optimised for processing with line-based tools such
as `jq <https://stedolan.github.io/jq/>`_.

.. code-block:: javascript

    {
      "playlist.title": "Winter Mix 3 - Too many words for their own good"
      "creator": "Jeffrey Lewis & Los Bolts",
      "title": "Avenue A, Shanghai, Hollywood",
      "musicbrainz.artist_id": "e1889f99-02fa-40aa-828c-4a74c255c568"
    }
    {
      "creator": "SKAndalous All-Stars",
      "title": "Age of Insects"
      "musicbrainz.artist_id": "bd9a7562-ee6f-41c0-a01b-da7119ef8f17",
      "musicbrainz.artist_country": "US"
    }
    {
      "creator": "Courtney Barnett",
      "title": "Lance Jr."
      "musicbrainz.artist_id": "55111838-f001-494a-a1b5-9d818db85810",
      "musicbrainz.artist_country": "AU"
    }

Schema
------

The Calliope playlist is formally defined by the following schema:

.. jsonschema:: ../calliope/playlist-item.jsonschema
