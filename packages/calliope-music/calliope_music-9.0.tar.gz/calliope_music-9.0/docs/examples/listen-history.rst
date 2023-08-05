Listening history examples
==========================

These examples use the :mod:`calliope.lastfm.history` module to query stored
plays from Last.fm.

You should first create a ``~/.config/calliope/calliope.conf`` file specifying
your last.fm username. For example:

.. code::

    [lastfm]
    user=bbc6music

Artists which you discovered this year
--------------------------------------

.. literalinclude:: ../../examples/listen_history/discovered-this-year.sh
    :start-after: set -e
    :language: bash

Music which you haven't listened to for over a year
---------------------------------------------------

.. literalinclude:: ../../examples/listen_history/not-listened-this-year.sh
    :start-after: set -e
    :language: bash

If you want to listen to this playlist, resolve the tracks using your local
music collection, for example:

.. code:: bash

   examples/listen_history/not-listened-this-year.sh | cpe tracker resolve-content - | cpe export -

.. _examples.listen-history.never-listened:

Music which you've never listened to
------------------------------------

.. literalinclude:: ../../examples/listen_history/never-listened.sh
    :start-after: set -e
    :language: bash

Music which you've listened to but don't own
--------------------------------------------

.. literalinclude:: ../../examples/listen_history/what-to-buy.sh
    :start-after: set -e
    :language: bash
