Importing online data
=====================

One of the primary goals of Calliope is to provide a unified interface and data
format for the varied online services related to music and metadata.

Most online services require an API key to access them. These are private tokens
which allow the service provider to monitor and control your usage. You will
need to obtain your own API keys to use these services. We try to document how
to do this, but be aware that service providers can change things without
warning.

Online collections
------------------

Collections from `Bandcamp <https://www.bandcamp.com/>`_ are available with the
:mod:`calliope.bandcamp` module or the :command:`cpe bandcamp` command. This
works without any API key.

The Spotify "My Library" tracks, albums and artists can be exported to and imported
from playlists with the :mod:`calliope.spotify` module or the `--library` switch
of the :command:`cpe spotify export` and :command:`cpe spotify import` commands.

Online playlists
----------------

Playlists from `Listenbrainz <https://listenbrainz.org/>`_ are available with
the :mod:`calliope.listenbrainz` module or the :command:`cpe listenbrainz`.

Playlists from `Spotify <https://www.spotify.com/>`_ are available with the
:mod:`calliope.spotify` module or the :command:`cpe spotify` command. A
:ref:`Spotify API key <api-keys.spotify>` is needed.

Playlists from `Youtube <https://www.youtube.com/>`_ are available with the
:mod:`calliope.youtube` module or the :command:`cpe youtube` command. A
Google API key for the Youtube Data API is needed.

Listen history
--------------

Listen history data from `Last.fm <https://www.last.fm>`_ can be exported
using the :mod:`calliope.lastfm.history` module or the :command:`cpe
lastfm-history` command.

Listen history data from `Listenbrainz <https://listenbrainz.org>`__ can be
exported using the :mod:`calliope.listenbrainz.listens` module or the
:command:`cpe listenbrainz-history` command.

Spotify doesn't make much listen history data available through their API.
It's possible to obtain the last year of history using the *Download your data*
option -- see Spotify's `'Data rights and privacy settings' guide
<https://support.spotify.com/us/article/data-rights-and-privacy-settings/>`_
for details.

Music metadata
--------------

Some metadata from `Last.fm <https://www.last.fm>`_ can be accessed with the
:mod:`calliope.lastfm` module or the :command:`cpe lastfm` command.

`Musicbrainz <https://www.musicbrainz.org/>`_ is a huge, open database of music
metadata. You can use the :mod:`calliope.musicbrainz` module or the
:command:`cpe musicbrainz` command to annotate playlist items with musicbrainz
IDs, metadata retrieved from musicbrainz and optionally update existing item data.
Items are only annotated automatically if a good enough match is found on
musicbrainz. In cases where the existing metadata is wrong or incomplete, use
the interactive mode to select the musicbrainz matches manually.
