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
Prototype of `cpe choose`, a constraint solving playlist creator.

Based on ideas from:

    https://www.researchgate.net/publication/220723500_Fast_Generation_of_Optimal_Music_Playlists_using_Local_Search

"""

import simpleai.search
import simpleai.search.viewers

import dataclasses
import logging
import random
import sys

log = logging.getLogger()


@dataclasses.dataclass
class Song():
    id : int
    title : str
    creator : str
    duration : int
    size : int
    familiar : float
    forgotten : float

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"𝄞{self.id}"


music_collection_small = [
    Song(1, "Punk Song 1", "Artist 1", 60, 1024, 0.2, 0.8),
    Song(2, "Punk Song 2", "Artist 1", 70, 1124, 0.2, 0.8),
    Song(3, "Jazz Song 1", "Artist 2", 500, 10240, 0.0, 0.0),
    Song(4, "Jazz Song 2", "Artist 2", 500, 10240, 0.0, 0.1),
    Song(5, "Pop Song 1", "Artist 3", 240, 4096, 0.9, 0.1),
    Song(6, "Pop Song 2", "Artist 3", 240, 4096, 0.85, 0.1),
]


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


class DurationConstraint():
    """Playlist should be a specified number of seconds in duration."""
    def __init__(self, duration_goal):
        self.goal = float(duration_goal)

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.goal})>"

    def score_playlist(self, playlist):
        duration = sum(s.duration for s in playlist)
        if duration <= self.goal:
            # 0 length playlist returns 0, GOAL length playlist returns 1
            score = duration / self.goal
        else:
            # playlist length >= 2 * duration returns 0.
            score = max((-duration + (2 * self.goal)), 0) / self.goal
        log.debug("%s: score %s for %s", self, score, duration)
        return score


class PlaylistGenerationProblem(simpleai.search.SearchProblem):
    """Create a playlist using local search algorithm."""
    def __init__(self, collection, constraints, initial_length=0):
        super(PlaylistGenerationProblem, self).__init__(initial_state=tuple())
        self.collection = collection
        self.constraints = constraints
        self.initial_length = initial_length

    def generate_random_state(self):
        state = tuple(random.sample(self.collection, self.initial_length))
        log.debug("initial state: %s", state)
        return state

    def actions(self, state):
        append = [AppendAction(s) for s in self.collection if s not in state]
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


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

viewer = simpleai.search.viewers.WebViewer()
viewer = None

constraints = [
    DurationConstraint(150)
]
problem = PlaylistGenerationProblem(music_collection_small, constraints, initial_length=3)

# This can go pretty wrong, with a duration constraint of 40 and iteration
# limit of 1000, making playlist with length 1540 !?!    10K iterations better.
#result = simpleai.search.local.simulated_annealing(problem, iterations_limit=10000, viewer=viewer)

# Works OK! With 1K iterations, still produces randomly bad results, e.g.
# duration of 1000 for a constraint of 800.
#result = simpleai.search.local.hill_climbing_stochastic(problem, iterations_limit=1000, viewer=viewer)

# Works OK! For simple cases goes straight and predictably to the right result.
result = simpleai.search.local.hill_climbing(problem, iterations_limit=100, viewer=viewer)

# Bad results with duration constraint of 40.
#result = simpleai.search.local.hill_climbing_random_restarts(problem, restarts_limit=100, iterations_limit=1000, viewer=viewer)

# These algorithms seem more expensive than the others.
#result = simpleai.search.local.beam(problem, iterations_limit=100, viewer=viewer)
#result = simpleai.search.local.beam_best_first(problem, iterations_limit=100, viewer=viewer)

print(result.state)
print(result.path())
print("Playlist duration: %s" % sum(s.duration for s in result.state))
