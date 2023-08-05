Making playlists
================

Everything in Calliope is a playlist, but some playlists are more enjoyable
than others.

Some commands in the :doc:`previous section <getting-data>` list a whole
music library. The commands in this section let you create interesting playlists
from those.

Shuffle
-------

A simple way to add interest is to randomize the order. Use :func:`calliope.shuffle.shuffle` or
:program:`cpe shuffle`. This produces a list of 10 random songs from your collection::

    cpe tracker tracks | cpe shuffle --count 10

Select
------

Calliope supports using constraint satisfaction to generate playlists. This is
done with the :func:`calliope.select.select` function or :command:`cpe select` command.

Diff
----

You can compare two playlists using :mod:`calliope.diff`. This is used in the example
:ref:`examples.listen-history.never-listened`.
