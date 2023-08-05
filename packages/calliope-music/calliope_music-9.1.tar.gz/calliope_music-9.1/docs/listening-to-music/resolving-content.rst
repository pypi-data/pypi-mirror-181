Resolving content
=================

    XSPF is an intermediate format. We expected a new kind of software called a
    content resolver to do the job of converting XSPF to a plain old list of
    files or URIs.

    -- The `XSPF specification <https://www.xspf.org/xspf-v1.html#rfc.section.3.2>`_, section 3.2.

Calliope aims to provide 'content resolver' functionality for playlists. This
means that based on the *identifier*, *creator*, *title* and *album* fields we
can resolve a *location*.

For local content, the :mod:`calliope.beets` and :mod:`calliope.tracker`
modules can resolve file:// URIs for playlist items.
