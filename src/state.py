

class State:

    def __init__(self, id, activities, representation, y_col, prediction='avg') -> None:
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
    

    def add_subseq_state(self, state_id):

        self.subsequent_states.append(state_id)

    def equals_state(self, activities):

        return self.activities == activities
    

    def predict(self, event):

        print(f"PREDICT -> INCIDENT: {event['Incident ID']} in STATE ID: {self.id}\n-- PE: {event['PrevEvents']}")

        return 1 # placeholder value


    def finalize(self):

        pass
        # print(f"Some method that prepares the state {self.id} bucket for prediction")
    








