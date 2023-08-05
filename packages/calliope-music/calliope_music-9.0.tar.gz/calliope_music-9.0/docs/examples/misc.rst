Miscellaneous examples
======================

Finding your most listened artists
----------------------------------

Using :command:`cpe lastfm` you can get a list of artists you listen to the most.
This is based on the data you have submitted to that service in the past.

.. code:: bash

    cpe lastfm top-artists

The Spotify online streaming service can provide a list of the artists
you listen to the most on that platform. See the list with:

.. code:: bash

    cpe spotify top-artists

Using :command:`cpe tracker` you can get a list of the top artists in your local
music collection. This is sorted by the number of tracks you have by that
artists rather than by how much you have listened to them:

.. code:: bash

    cpe tracker top-artists

Follow your top artists on Twitter
----------------------------------

See above for how to get a list of top artists.

Now pipe that list to ``cpe musicbrainz --include urls`` and you'll get a list
of relationship URLs for each artist.

Finally, pipe that into ``jq``:

.. code:: bash

    jq '. | ."musicbrainz.artist.urls" // [] | .[]."musicbrainz.url.target" | "@" + match("^http[s]?://(www\\\.)?twitter.com/(.*)").captures[1].string' -r |sort -u

Now you have a list of Twitter handles. Using a tool such as
`[t (Twitter CLI) <https://github.com/sferik/t>`_ you can add all these handles
to a list, or you can just follow all of them directly. Note that you have to
fill in a bunch of forms in order to get a Twitter API key before you can use a
Twitter CLI tool. The ``t authorize`` command will point you in the right
direction.
