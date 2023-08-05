Importing local data
====================

Local music collection
----------------------

The `Beets music organiser <http://beets.io/>`_ is recommended for large music
collections. You can use :mod:`calliope.beets` or :program:`cpe beets` to
list the contents of the Beets library.

Linux desktop users who have the `Tracker search engine
<https://gnome.pages.gitlab.gnome.org/tracker/>`_ installed can use
:mod:`calliope.tracker` or :program:`cpe tracker` to list local music files.

Playlists stored as files
-------------------------

Use the :func:`calliope.import_.import_` function, or the :program:`cpe import`
command to load playlist files.

I recommend that you store your playlists in `XSPF <https://www.xspf.org/>`_
format. It's the most flexible and widely supported playlist format I know of.

Playlists from applications
---------------------------

Most apps can import and export playlists in a format Calliope can read.

  * Rhythmbox: the `Playlists import/export plugin
    <https://github.com/petko10/rhythmbox-plugin-playlists-import-export>`_ may
    be useful.
