Examples for Music Collectors
=============================

Keeping a collection of your own digital music is fun and exciting. Calliope
integrates with multiple tools for managing a local music collection - choose
one :doc:`from this list here </getting-data/local>`.

Online collection to local collection
-------------------------------------

I download albums from my :doc:`online music collection </getting-data/online>`
but sometimes I miss them. This example lists all the albums I've bought on
Bandcamp that aren't available locally.

The script resolves Musicbrainz identifiers from the Bandcamp metadata, because
otherwise there are a lot of false negatives from things like "Pictish Trail" vs
"The Pictish Trail", or "Catbite (EP)" vs "Catbite".

.. literalinclude:: ../../examples/collectors/online-to-local.sh
    :start-after: set -e
    :language: bash
