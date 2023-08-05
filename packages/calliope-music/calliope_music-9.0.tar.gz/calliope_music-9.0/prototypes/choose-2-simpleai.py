# Copyright (C) 2020  Sam Thursfield <sam@afuera.me.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Prototype #2 of `cpe choose`, a constraint solving playlist creator.

Based on ideas from:

    https://www.researchgate.net/publication/220723500_Fast_Generation_of_Optimal_Music_Playlists_using_Local_Search

Compared to prototype 1, this loads real playlists and is tested with a list
of 3.2K albums.

"""

import simpleai.search
import simpleai.search.viewers

import calliope

import argparse
import dataclasses
import logging
import pathlib
import random
import sys

log = logging.getLogger()

MINUTES = 60
MSEC = 1000

class AppendAction():
    def __init__(self, song):
        self.song = song

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.song.id})>"

    def apply(self, state):
        return state + (self.song,)


class RemoveAction():
    def __init__(self, index):
        self.index = index

    def __repr__(self):
        return f"<{self.__class__.__name__}(index={self.index})>"

    def apply(self, state):
        return state[0:self.index] + state[self.index+1:]


class Constraint():
    """Base class for constraints on a playlist."""
    def __init__(self, prop, vmin, vmax):
        self.prop = prop
        self.vmin = float(vmin)
        self.vmax = float(vmax)
        assert self.vmax > 0
        assert self.vmax >= self.vmin

    def __repr__(self):
        if self.vmin == self.vmax:
            return f"<{self.__class__.__name__}({self.prop}={self.vmax})>"
        else:
            return f"<{self.__class__.__name__}({self.vmin}<={self.prop}<={self.vmax})>"

    def partition(self, collection):
        """Divide 'collection' into 3 partitions 'too-low', 'good', 'too-high'.

        This is used to define the neighbourhood we search for a solution.

        """
        too_low = [s for s in collection if s[self.prop] < self.vmin]
        good = [s for s in collection if s[self.prop] >= self.vmin and s[self.prop] <= self.vmax]
        too_high = [s for s in collection if s[self.prop] > self.vmax]
        return too_low, good, too_high


class EachGlobalConstraint(Constraint):
    """For each song, 'prop' should be between 'vmin' and 'vmax'."""

    def score_item(self, item):
        value = item[self.prop]
        # Return 1.0 if vmin <= value <= vmax, decreasing to 0.0 as value tends
        # towards 0.0 and vmax*2.
        if self.vmin > 0 and value <= self.vmin:
            score = value / self.vmin
        elif value >= self.vmax:
            score = max((-value + (2 * self.vmax)), 0) / self.vmax
        else:
            score = 1.0
        return score

    def score_playlist(self, playlist):
        if len(playlist) == 0:
            return 0.0
        else:
            score = sum(self.score_item(s) for s in playlist) / len(playlist)
            log.debug("%s: score %s", self, score)
            return score


class SumGlobalConstraint(Constraint):
    """The sum of 'prop' for all songs should be between 'vmin' and 'vmax'."""
    def score_playlist(self, playlist):
        value = sum(s[self.prop] for s in playlist)
        # Return 1.0 if vmin <= value <= vmax, decreasing to 0.0 as value tends
        # towards 0.0 and vmax*2.
        if self.vmin > 0 and value <= self.vmin:
            score = value / self.vmin
        elif value >= self.vmax:
            score = max((-value + (2 * self.vmax)), 0) / self.vmax
        else:
            score = 1.0
        log.debug("%s: score %s for %s", self, score, value)
        return score


class ItemDurationConstraint(EachGlobalConstraint):
    """Each song should have duration in range [min, max]."""
    def __init__(self, vmin, vmax):
        EachGlobalConstraint.__init__(self, prop='duration', vmin=vmin, vmax=vmax)


class PlaylistDurationConstraint(SumGlobalConstraint):
    """Playlist should be a specified number of seconds in duration."""
    def __init__(self, vmin, vmax):
        SumGlobalConstraint.__init__(self, prop='duration', vmin=vmin, vmax=vmax)


class PlaylistDiskSpaceConstraint(SumGlobalConstraint):
    """Playlist items should be a specified number of bytes in size."""
    def __init__(self, vmin, vmax):
        SumGlobalConstraint.__init__(self, prop='album.size_mb', vmin=vmin, vmax=vmax)


class PlaylistGenerationProblem(simpleai.search.SearchProblem):
    """Create a playlist using local search algorithm."""
    def __init__(self, collection, constraints, initial_length=0):
        super(PlaylistGenerationProblem, self).__init__(initial_state=tuple())
        self.collection = collection
        self.constraints = constraints
        self.initial_length = initial_length

        self.partitions_low = []
        self.partitions_good = []
        self.partitions_high = []
        for i, constraint in enumerate(self.constraints):
            too_low, good, too_high = constraint.partition(collection)
            self.partitions_low.append(too_low)
            self.partitions_good.append(good)
            self.partitions_high.append(too_high)

    def generate_random_state(self):
        state = tuple(random.sample(self.collection, self.initial_length))
        log.debug("initial state: %s", state)
        return state

    def make_append_action_from_partition(self, state, append_list, partition):
        # Pop item from a partition to form part of the current neighbourhood.
        # Disallow anything that's already in the list.
        while len(partition) > 0:
            item = partition.pop()
            if item not in state:
                append_list += [AppendAction(item)]
                break

    def actions(self, state):
        append = []
        for p in self.partitions_low + self.partitions_high:
            self.make_append_action_from_partition(state, append, p)
        for p in self.partitions_good:
            for i in range(0,4):
                self.make_append_action_from_partition(state, append, p)
        if len(state) > 0:
            remove = [RemoveAction(i) for i in range(0, len(state))]
        else:
            remove = []
        possible_actions = append + remove
        #random.shuffle(possible_actions)
        log.debug("actions with len %s: %s", len(state), possible_actions)
        return possible_actions

    def result(self, state, action):
        return action.apply(state)

    def value(self, state):
        return sum(c.score_playlist(state) for c in self.constraints)


def argument_parser():
    parser = argparse.ArgumentParser(
        description="Playlist generator prototype #2")
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help="Enable detailed logging to stderr")
    parser.add_argument('playlist', type=pathlib.Path)
    return parser


def load_collection(path):
    music_collection = set()
    if path.name == '-':
        f = sys.stdin
    else:
        f = open(path)
    for i, item in enumerate(calliope.playlist.read(f)):
        # Temporary workaround -- it might be better to generate
        # 'universal' ids from track metadata, in future.
        if 'id' not in item:
            item['id'] = str(i)
        music_collection.add(item)
    # splitstream closes the stream for us.
    return music_collection


def main():
    args = argument_parser().parse_args()

    if args.debug:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    viewer = simpleai.search.viewers.WebViewer()
    viewer = None

    music_collection = load_collection(args.playlist)

    constraints = [
        ItemDurationConstraint(30 * MINUTES * MSEC, 70 * MINUTES * MSEC),  # 30-70 min
        PlaylistDurationConstraint(6 * 60 * MINUTES * MSEC, 6 * 60 * MINUTES * MSEC),  # 6 hrs
        PlaylistDiskSpaceConstraint(0, 600),  # 600 MB
    ]

    problem = PlaylistGenerationProblem(music_collection, constraints, initial_length=6)

    # This can go pretty wrong, with a duration constraint of 40 and iteration
    # limit of 1000, making playlist with length 1540 !?!    10K iterations better.
    #result = simpleai.search.local.simulated_annealing(problem, iterations_limit=10000, viewer=viewer)

    # Works OK! With 1K iterations, still produces randomly bad results, e.g.
    # duration of 1000 for a constraint of 800.
    #result = simpleai.search.local.hill_climbing_stochastic(problem, iterations_limit=1000, viewer=viewer)

    # Works OK! For simple cases goes straight and predictably to the right result.
    result = simpleai.search.local.hill_climbing(problem, iterations_limit=1000, viewer=viewer)

    # Bad results with duration constraint of 40.
    #result = simpleai.search.local.hill_climbing_random_restarts(problem, restarts_limit=100, iterations_limit=1000, viewer=viewer)

    # These algorithms seem more expensive than the others.
    #result = simpleai.search.local.beam(problem, iterations_limit=100, viewer=viewer)
    #result = simpleai.search.local.beam_best_first(problem, iterations_limit=100, viewer=viewer)

    log.info(result.state)
    log.info(result.path())

    comments = [f"Generated by {__file__}"]
    duration = sum(s['duration'] for s in result.state) / 1000.0
    comments.append("Playlist duration: %s sec (%f min)" % (duration, duration / 60.0))
    size_mb = sum(s['album.size_mb'] for s in result.state)
    comments.append("Playlist size: %s MB" % (size_mb))
    if len(result.state) > 0:
        first_track = result.state[0]
        first_track['playlist.comments'] = comments
    calliope.playlist.write(result.state, sys.stdout)


try:
    main()
except RuntimeError as e:
    sys.stderr.write("ERROR: {}\n".format(e))
    sys.exit(1)
