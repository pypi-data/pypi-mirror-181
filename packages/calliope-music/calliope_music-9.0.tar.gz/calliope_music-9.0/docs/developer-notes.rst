Notes for developers working on Calliope itself
===============================================

Tests for web service integration
---------------------------------

Automated tests should not run against a real web service, for reliability
and performance reasons. Here are examples of how web APIs can be mocked in Calliope test
suite. There are several methods, as most integrations use a third-party helper library
rather than talking directly to the remote service.

Run a local HTTP server
~~~~~~~~~~~~~~~~~~~~~~~

This method is used by ``test_lastfm_history.py``.
Python ``wsgiref.simple_server`` runs a real HTTP server, and the address is
passed to ``cpe lastfm-history`` command with the ``--server`` argument.

Override the urllib Opener class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method is used by ``test_musicbrainz.py``, adapted from the testsuite of
the Python ``musicbrainzngs`` module. An internal function from ``musicbrainzngs``
is monkeypatched to use our custom URL opener. Testcases supply a map of URL
patterns as regular expressions and functions which simulate the response.

Override the public API of the client library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method is used by ``test_spotify.py``. The whole :class:`calliope.spotify.SpotifyContext`
class is replaced with a ``unittest.mock.Mock`` instance, allowing us to replace the Spotipy client
library completely with our own functions.
