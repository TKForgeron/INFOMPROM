

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

        # if self.rep == 'trace':
        #     return self.activities == activities
        # elif self.rep == 'set':
        #     return set(sorted(activities)) == set(sorted(self.activities))
        # elif self.rep == 'multiset':
        #     return sorted(activities) == sorted(self.activities)


        self.subsequent_states.append(state_id)

    
    def equals_state(self, activities):

        if self.rep == 'trace':
            return self.activities == activities
        elif self.rep == 'set':
            return set(sorted(activities)) == self.activities
        elif self.rep == 'multiset':
            return sorted(activities) == self.activities
        



