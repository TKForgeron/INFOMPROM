import sys
import pandas as pd
from state import State


class ATS:

    # TODO: Make it work for set and multiset configuration
    # TODO: Make it annotated
    # TODO: predictive measures

    def __init__(
        self,
        trace_id_col: str,
        act_col: str,
        representation: str = "trace",
        horizon: int = sys.maxsize,
        filter_out: list = [],
    ) -> None:

        self.trace_id_col = trace_id_col
        self.act_col = act_col

        self.rep = representation
        self.horizon = horizon
        self.filter_out = filter_out

        empty_state = State(0, [], representation)
        self.states = [empty_state]

    def check_subseq_states(self, activities: str, state_ids: int) -> int:
        """
        This function checks whether there is a subsequent state that could be accessed
        for the given trace. Makes sure that no more states then necessary will be created.

        Parameters
        ----------
            activities : [str]
                Activities that, together, form a state.
            state_ids : [int]
                ids from subsequent states in the current state.

        """

        if not state_ids:
            return -1

        for id in state_ids:

            if self.states[id].equals_state(activities):
                return id

        return -1

    def check_existing_states(self, activities: str, state_ids: list[str]) -> int:
        """
        This function checks whether there is a state that could be used
        for the given trace. It will first look into the subsequent states before it will look
        in all existing states. Makes sure that no more states then necessary will be created.

        Parameters
        ----------
            activities : [str]
                Activities that, together, form a state.
            state_ids : [int]
                ids from subsequent states in the current state.

        """

        # TODO: we need to check whether it is faster to only check all states immediately
        # Look into subsequent_states first for computational reasons
        for id in state_ids:
            if self.states[id].equals_state(activities):
                return (id, False)

        # for state in self.states:
        for id, state in enumerate(self.states):

            if state.equals_state(activities):
                print(f"found id: {id}")
                return (id, True)

        return (-1, True)

    def create_state(self, activities: list[str]):
        """
        This function creates a new state object.

        Parameters
        ----------
            activities : [str]
                Activities that, together, form a state.
        """

        state_id = len(self.states)

        self.states.append(State(state_id, activities, self.rep))

        return state_id

    def print_state(self, state):
        """
        Small debugging function that prints the details of a state.

        Parameters
        ----------
            state : State()
                State object
        """

        print(f"id: {state.id}")
        print(f"act: {state.activities}")
        print("-------------------------------------\n")

    def transform_rep(self, act):

        # filtering | TODO: we might want to do this for the trace once using pd.filter()
        act = [x for x in act if x not in self.filter_out]

        # horizon
        act = act[-self.horizon :]

        # representation
        if self.rep == "set":
            act = list(set(sorted(act)))
        elif self.rep == "multiset":
            act = sorted(act)

        return act.copy()

    def add_trace(self, trace: list[dict]):
        """
        This function, given a trace (i.e., events that belong to the same incident),
        creates all the required states.

        Parameters
        ----------
            trace : [{}]
                Events that belong to the same trace
        """

        activities = []

        curr_state = self.states[0]
        curr_state.add_event(trace[0])

        for event in trace:

            activities.append(event[self.act_col])

            activities = self.transform_rep(activities.copy())

            next_state_id, make_new_edge = self.check_existing_states(
                activities, curr_state.subsequent_states
            )

            # next state does not yet exist
            if make_new_edge:

                if next_state_id < 0:
                    state_id = self.create_state(activities.copy())
                else:
                    state_id = next_state_id

                curr_state.add_subseq_state(
                    state_id
                )  # <<<<<<<<<<werk je overal met inplace?>>>>>>>>>>

            curr_state = self.states[next_state_id]

            curr_state.add_event(event)

    def create_ATS(self, df: pd.DataFrame):
        """
        Main function that creates the ATS given an event log.

        Parameters
        ----------
            df : pd.Dataframe
                The event log
        """

        grouped = df.groupby(self.trace_id_col)

        for name, group in grouped:
            self.add_trace(group.to_dict("records"))

    def print(self):
        """

        Function that prints the (Annotated) Transition System to
        a TXT file. Right now, merely for debugging purposes.

        """

        with open("data/ATS_output.txt", "w") as text_file:

            for state in self.states:

                print(f"id: {state.id}", file=text_file)
                print(f"activities: {state.activities}", file=text_file)

                print(f"subseq: {state.subsequent_states}", file=text_file)

                print("Data:", file=text_file)

                for row in state.data:

                    print(row, file=text_file)

                print("\n--------------------------------------\n", file=text_file)
