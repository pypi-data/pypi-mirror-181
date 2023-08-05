Exporting playlists
===================

The :mod:`calliope.export` module and :command:`cpe export` command supports
writing playlists to various formats.

Exporting to applications
-------------------------

You may pipe output from :command:`cpe export` straight into a suitable
application.

Rhythmbox
^^^^^^^^^

Rhythmbox exposes a D-Bus method that imports playlists. Install the
`rhythmbox-load-playlists script <https://github.com/ssssam/dotfiles/blob/main/bin/rhythmbox-load-playlist.sh>`_
so you can pipe playlists straight into Rhythmbox::

    ... | cpe export - | rhythmbox-load-playlists
