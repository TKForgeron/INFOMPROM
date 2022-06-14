<<<<<<< HEAD
<<<<<<< HEAD


class State:

    def __init__(self, id, activities, representation, y_col, prediction='avg') -> None:
=======
=======
>>>>>>> ed9eb8b14fa5cf882e64d0ca9c3c7ff119ed63b0
from decimal import ROUND_DOWN
from multiprocessing.dummy import JoinableQueue
from time import time


class State:
    def __init__(self, id, activities, representation) -> None:
>>>>>>> ed9eb8b14fa5cf882e64d0ca9c3c7ff119ed63b0
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

        self.data = [] # must be replaced by the bucket | y_col and prediction can be used for init
        self.subsequent_states = []

    def add_event(self, row):

        self.data.append(row)
        pass
<<<<<<< HEAD
<<<<<<< HEAD
    
=======
>>>>>>> ed9eb8b14fa5cf882e64d0ca9c3c7ff119ed63b0
=======
>>>>>>> ed9eb8b14fa5cf882e64d0ca9c3c7ff119ed63b0

    def add_subseq_state(self, state_id):

        self.subsequent_states.append(state_id)

    def equals_state(self, activities):

        return self.activities == activities
<<<<<<< HEAD
<<<<<<< HEAD
    

    def predict(self, event):

        print(f"PREDICT -> INCIDENT: {event['Incident ID']} in STATE ID: {self.id}\n-- PE: {event['PrevEvents']}")

        return 1 # placeholder value


    def finalize(self):

        pass
        # print(f"Some method that prepares the state {self.id} bucket for prediction")
    








=======
=======
>>>>>>> ed9eb8b14fa5cf882e64d0ca9c3c7ff119ed63b0

        # if self.rep == 'trace':
        #     return self.activities == activities
        # elif self.rep == 'set':
        #     return set(sorted(activities)) == self.activities
        # elif self.rep == 'multiset':
        #     return sorted(activities) == self.activities
<<<<<<< HEAD
>>>>>>> ed9eb8b14fa5cf882e64d0ca9c3c7ff119ed63b0
=======
>>>>>>> ed9eb8b14fa5cf882e64d0ca9c3c7ff119ed63b0
