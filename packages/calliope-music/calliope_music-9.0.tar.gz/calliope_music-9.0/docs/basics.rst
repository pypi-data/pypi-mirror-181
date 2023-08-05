The basics
==========

All Calliope commands operate on *Calliope playlists*. These are very similar
to `XSPF playlists <https://calliope-music.readthedocs.io/en/latest/>`_, but
using the `JSON lines <https://calliope-music.readthedocs.io/en/latest/>`_
format so that they are nice to process with line-based commandline tools.

Here is an example of a simple Calliope playlist:

.. code:: javascript

    { "creator": "The Mighty Mighty Bosstones", "title": "The Impression That I Get" }
    { "creator": "Less Than Jake", "title": "Gainesville Rock City" }

Calliope commands are designed to be combined with each other, with the
data processing tools `jq <https://stedolan.github.io/jq/>`_ and
`yq <https://github.com/kislyuk/yq>`_, and with other UNIX shell tools.
Most commands default to reading playlists on stdin and writing processed
playlists on stdout.

Run ``cpe`` to see the list of commands available.
