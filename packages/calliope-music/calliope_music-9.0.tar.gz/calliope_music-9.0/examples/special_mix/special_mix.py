"""
Special mix
===========

An example of generating personalised playlists based on a user's listening
history.

The idea of Special Mix is: create a 60 minute playlist, taking a specific
year of listen-history as the starting point.

Usage
-----

The example can be run from the ``calliope_examples`` package when installed:

.. code:: bash

    python3 -m calliope_examples.special_mix ...

You'll need to choose and configure a listen history provider.  Listen history
can be fetched using any of the
:func:`calliope.available_listen_history_providers` classes.
An example of using :mod:`calliope.listenbrainz.listens` to fetch Listenbrainz history:

.. code:: bash

    ... --history-provider=listenbrainz_history --history-provider-args="username=mylistenbrainzusername"

You also need to choose and configure a content resolver.  Playable tracks can
be resolved using any of the :func:`calliope.available_content_resolvers` classes.

An example using :mod:`calliope.tracker` to resolve tracks to locally available music:

.. code:: bash

    ... --resolver=tracker

An example using :mod:`calliope.spotify` to resolve tracks to Spotify:

.. code:: bash

    # Make sure `calliope.conf` exists and defines spotify API key, etc.
    ... --resolver=spotify --resolver-args=user=myspotifyusername

Notes
-----

Listen history needs to be synced, and the initial sync can take a long time
if there is a lot of history.

All candidate tracks are resolved before generating the playlist, as the
``select`` module needs to know the track durations in advance. This can make
execution take a long time. Caching means that it should be faster once it has
run a few times.

If none of the tracks from listen history can be resolved, the output will
be an empty playlist.

"""

import click

from datetime import date, datetime, timedelta
import logging
import os
import pathlib
import random
import sys

import calliope

log = logging.getLogger()


DURATION = 60 * 60


class ConfigError(Exception):
    pass


class Config(calliope.config.Configuration):
    """Config is stored in 'special_mix' section of calliope.conf"""

    def __init__(self, sync=True, history_provider=None,
                 history_provider_args=None, resolver=None,
                 resolver_args=None):
        super(Config, self).__init__()

        self._sync = sync

        log.info(f"Using history provider: '{history_provider}'")
        self._history_class = calliope.available_listen_history_providers()[history_provider]
        if self._history_class is None:
            raise RuntimeError(f"History provider class {history_provider} is not available.")

        history_config = self.get_section(history_provider)
        for arg in history_provider_args:
            var, value = arg.split('=', 1)
            history_config[var] = value
        self._history_config = history_config

        log.info(f"Using resolver: '{resolver}'")
        self._resolver_class = calliope.available_content_resolvers()[resolver]
        if self._resolver_class is None:
            raise RuntimeError(f"Resolver class {resolver} is not available.")

        resolver_config = self.get_section(resolver)
        for arg in resolver_args:
            var, value = arg.split('=', 1)
            resolver_config[var] = value
        self._resolver_config = resolver_config

    def content_resolver(self):
        return self._resolver_class(**self._resolver_config)

    def history_provider(self):
        return self._history_class(**self._history_config)

    def sync(self):
        return self._sync


class PlaylistGenerator():
    def __init__(self, config: Config):
        self.config = config

    def setup_content_resolver(self):
        self.content_resolver = self.config.content_resolver()
        self.content_resolver.authenticate()

    def setup_listen_history(self):
        self.listen_history = self.config.history_provider()

        if self.config.sync():
            log.info("Syncing from listen history provider")
            sync_op = self.listen_history.prepare_sync()
            for page in sync_op.pages():
                sync_op.process_page(page)


class DiscoveredInTimePeriod(PlaylistGenerator):
    """
    Tracks where first play was in specified time period.
    """

    def __init__(self, config: Config, span='year', period=None, minimum_tracks=100):
        super(DiscoveredInTimePeriod, self).__init__(config)
        self.span = span
        self.period = None
        self.minimum_tracks = 100

    def _add_year(self, d):
        try:
            return d.replace(year = d.year + 1)
        except ValueError:
            return d + (date(d.year + 1, 1, 1) - date(d.year, 1, 1))

    def setup(self):
        log.debug(f"{__class__}.setup()")
        self.setup_content_resolver()
        self.setup_listen_history()

    def run(self):
        histogram = self.listen_history.histogram(bucket=self.span)

        if self.period is None:
            active_periods = list(sorted(
                entry.bucket
                for entry in histogram if entry.count > self.minimum_tracks
            ))
            log.debug(f"Choose one period from: {active_periods}")
            if len(active_periods) == 0:
                raise RuntimeError("No listen history data is available.")
            self.period = random.choice(active_periods)

        period_start = datetime.fromisoformat(self.period)
        period_end = self._add_year(period_start)

        log.info("Query tracks for period %s -> %s", period_start, period_end)
        all_tracks = list(self.listen_history.tracks(
            first_play_since=period_start, first_play_before=period_end))
        log.info("Tracks: %i", len(all_tracks))

        resolved_tracks = list(self.content_resolver.resolve_content(all_tracks))

        tracks_with_durations = [
            t for t in resolved_tracks if 'duration' in t and 'location' in t
        ]
        log.info("Tracks with location and duration resolved: %i", len(tracks_with_durations))

        constraints = [
            calliope.select.constraints.PlaylistDurationConstraint(
                DURATION * 1000, DURATION * 1000
            )
        ]

        playlist = list(calliope.select.select(
            calliope.shuffle.shuffle(tracks_with_durations),
            constraints
        ))

        if len(playlist) == 0:
            raise RuntimeError("Empty playlist generated.")

        playlist[0]['playlist.title'] = f"Discoveries of {period_start.year}"
        playlist[0]['playlist.generator'] = "special_mix.DiscoveredInTimePeriod"

        return playlist


@click.command()
@click.argument("output", type=click.File(mode='w'), default='-')
@click.option("--debug", is_flag=True, help="Enable detailed logging to stderr")
@click.option('--random-seed', '-s', type=int, help="Use fixed random number seed.")
@click.option('--history-provider', '-h', default='listenbrainz_history',
              type=click.Choice(calliope.available_listen_history_providers().keys()),
              help="Module to use for fetching listen history")
@click.option('--history-provider-args', '--ha',
              type=str, multiple=True,
              help="Listen history configuration. Example for the `listenbrainz` resolver: --history-provider-args=username=myusername")
@click.option('--resolver', '-r', default='tracker',
              type=click.Choice(calliope.available_content_resolvers().keys()),
              help="Module to use for resolving playable track locations")
@click.option('--resolver-args', '--ra',
              type=str, multiple=True,
              help="Resolver-specific configuration. Example for the `spotify` resolver: --resolver-args=user=ssssam")
@click.option('--sync', is_flag=True, default=True, help="Sync listen history on startup")
def main(
    output, debug, random_seed, history_provider, history_provider_args,
    resolver, resolver_args, sync
):
    if debug:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    config = Config(
        sync=sync, history_provider=history_provider,
        history_provider_args=history_provider_args, resolver=resolver,
        resolver_args=resolver_args
    )

    pl = DiscoveredInTimePeriod(config)
    pl.setup()
    playlist = list(pl.run())

    calliope.playlist.write(playlist, output)


try:
    main()
except RuntimeError as e:
    sys.stderr.write("ERROR: {}\n".format(e))
    sys.exit(1)
