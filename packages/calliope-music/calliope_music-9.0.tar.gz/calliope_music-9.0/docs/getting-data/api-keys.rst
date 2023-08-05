API keys
========

Online service providers usually want to know which apps are accessing
their APIs, so they require each app to authenticate using a private
API key.

Calliope is an open-source toolkit, so by definition we cannot distribute
API keys ourselves. This section documents how to obtain your own API keys
for some service providers and use them with Calliope.

Please file a `merge request <https://gitlab.com/samthursfield/calliope/-/merge_requests>`_ or
`issue <https://gitlab.com/samthursfield/calliope/-/issues>`_ if you find that
this information is out of date.

.. _api-keys.spotify:

Spotify
-------

You will need an API key to access Spotify. This is free of charge and is
done by registering a Spotify application as follows:

  1. Log in with a Spotify user account and register at the
     `My Dashboard <https://developer.spotify.com/dashboard/applications>`_ page.

  2. Click 'Create an app'. Choose a name and description that makes sense for you.

  3. Click on the app name. Copy the client ID and client secret.

  4. Click 'Edit settings' and add ``http://localhost:8080/`` to the 'Redirect URIs' list.

You can now save this information to the Calliope config file used by the CLI, usually
``$HOME/.config/calliope/calliope.conf``. Here's an example:

.. code::

    [spotify]
    client-id = 044a880f7e989352f1d243e39648e653
    client-secret = 54967576893ae3f9c3568a1977016e8d
    redirect-uri = http://localhost:8080/

When you next run a :command:`cpe spotify` subcommand, Calliope will
authenticate with Spotify using a `local HTTP server <https://github.com/plamere/spotipy/pull/243>`_.
