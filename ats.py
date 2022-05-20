import pandas as pd
from typing import List
from state import State


class ATS:

    # TODO: Make it work for set and multiset configuration
    # TODO: Make it annotated
    # TODO: predictive measures

    def __init__(self, trace_id_col: str, act_col: str, representation: str) -> None:

        self.trace_id_col = trace_id_col
        self.act_col = act_col
        self.rep = representation
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

    def create_state(self, activities: List[str]):
        """
        This function creates a new state object.

        Parameters
        ----------
            activities : [str]
                Activities that, together, form a state.
        """

        if self.rep == "set":
            activities = set(sorted(activities))
        elif self.rep == "multiset":
            activities = sorted(self.activities)

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

    def add_trace(self, trace: dict):
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

            next_state_id = self.check_subseq_states(
                activities, curr_state.subsequent_states
            )

            # next state does not yet exist as subsequent state of current state
            if next_state_id < 0:
                state_id = self.create_state(activities.copy())
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

        with open("Output.txt", "w") as text_file:

            for state in self.states:

                print(f"id: {state.id}", file=text_file)
                print(f"activities: {state.activities}", file=text_file)

                print(f"subseq: {state.subsequent_states}", file=text_file)

                print("Data:", file=text_file)

                for row in state.data:

                    print(row, file=text_file)

                print("\n--------------------------------------\n", file=text_file)
