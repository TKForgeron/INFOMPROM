from decimal import ROUND_DOWN
from multiprocessing.dummy import JoinableQueue
from time import time


class State:
    def __init__(self, id, activities, representation) -> None:
        """
        Constructs a new state object.

        Parameters
        ----------
            activities : [str]
                The activities that make up the state.
        """

        self.activities = activities
        self.rep = representation
        self.id = id

        self.data = []
        self.subsequent_states = []

    def add_event(self, row):

        self.data.append(row)
        pass

    def add_subseq_state(self, state_id):

        self.subsequent_states.append(state_id)

    def equals_state(self, activities):

        return self.activities == activities

        # if self.rep == 'trace':
        #     return self.activities == activities
        # elif self.rep == 'set':
        #     return set(sorted(activities)) == self.activities
        # elif self.rep == 'multiset':
        #     return sorted(activities) == self.activities
