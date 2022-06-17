import sys
import pandas as pd
from src.state import State
from src.helper import printProgressBar
import pickle


class ATS:
    def __init__(
        self,
        trace_id_col: str,
        act_col: str,
        y_col: str,
        representation: str = "trace",
        horizon: int = sys.maxsize,
        filter_out: list = [],
        encoding_operation: str = None,
        model_type: str = None,
        seed: int = 42,
        cv: int = 5,
    ) -> None:

        print("START CREATING ATS")

        self.trace_id_col = trace_id_col
        self.act_col = act_col

        self.rep = representation
        self.horizon = horizon
        self.filter_out = filter_out

        self.model_type = model_type
        self.y_col = y_col

        empty_state = State(
            0, [], representation, y_col, encoding_operation, model_type, seed, cv
        )
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
                return (id, True)

        return (-1, True)

    def create_state(self, activities: list[str]) -> int:
        """
        This function creates a new state object.

        Parameters
        ----------
            activities : [str]
                Activities that, together, form a state.

        Returns
        ----------

            state_id : int
                Id of the created state
        """

        state_id = len(self.states)
        self.states.append(
            State(
                state_id, activities, self.rep, self.y_col, model_type=self.model_type
            )
        )

        return state_id

    def transform_rep(self, act: list[str]) -> list[str]:

        # filtering | TODO: we might want to do this for the trace once using pd.filter()
        act = [x for x in act if x not in self.filter_out]

        # horizon
        act = act[-self.horizon :]

        # representation
        if self.rep == "set":
            act = sorted(list(set(act)))
        elif self.rep == "multiset":
            act = sorted(act)

        return act.copy()

    def add_trace(self, trace: list[dict]) -> None:
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

    def create_ATS(self, df: pd.DataFrame) -> None:
        """
        Main function that creates the ATS given an event log.

        Parameters
        ----------
            df : pd.Dataframe
                The event log
        """

        grouped = df.groupby(self.trace_id_col)

        length = len(grouped)
        i = 0

        printProgressBar(0, length, prefix="Create:", suffix="Complete", length=50)
        for name, group in grouped:
            self.add_trace(group.to_dict("records"))

            printProgressBar(
                i + 1, length, prefix="Create:", suffix="Complete", length=50
            )
            i += 1

        print("\n")

    def print(self) -> None:
        """

        Function that prints the (Annotated) Transition System to
        a TXT file. Right now, merely for debugging purposes.

        """

        with open("data/ATS_output.txt", "w") as text_file:

            printProgressBar(
                0, len(self.states), prefix="Print:", suffix="Complete", length=50
            )

            for i, state in enumerate(self.states):

                printProgressBar(
                    i, len(self.states), prefix="Print:", suffix="Complete", length=50
                )
                print(f"id: {state.id}", file=text_file)
                print(f"activities: {state.activities}", file=text_file)

                print(f"Subseq: {state.subsequent_states}", file=text_file)

                print("Data:", file=text_file)

                for row in state.bucket.data:

                    print(row, file=text_file)

                print("\n--------------------------------------\n", file=text_file)

        print("\n")  # some weird bug in the progress

    def traverse_ats(self, event: dict) -> float:

        """

        Function that traverses the ats to find the bucket that must
        be used for predicting the given event.


        Parameters
        ----------
            event : dict
                A single event

        Returns
        ----------

            y : float
                Predicted value

        """

        search_term = []
        state = self.states[0]
        state_id = 0

        # print("\n--------------------------------")
        # print(f"ID: {event['Incident ID']} acts: {event['PrevEvents']}")

        for l in range(1, len(event["PrevEvents"]) + 1):

            sub_seq = state.subsequent_states

            search_term = event["PrevEvents"][:l]
            search_term = self.transform_rep(search_term)
            # print(f"o- ST: {search_term}  ")

            next_state = 0

            for s in sub_seq:
                # print(f"--- RESEARCH state {s}: {self.states[s].activities}")
                if self.states[s].activities == search_term:
                    state = self.states[s]
                    state_id = s
                    next_state = 1
                    break

            # if next_state == 0:
            #     print(f"NOTHING FOUND. Finished with state {state_id}")
            # else:
            #     print(f"NEXT -> ID: {state_id} | SA: {state.activities}")

            if event["PrevEvents"] == state.activities or next_state == 0:
                # print(f"(OPTIMAL) STATE {state_id} FOR PREDICTION FOUND!")

                return state.predict(event)

        return state.predict(event)

    def finalize(self) -> None:
        """
        This function finalizes the ATS such that can work as
        a prediction model.

        """

        printProgressBar(
            0, len(self.states), prefix="Finalize:", suffix="Complete", length=50
        )

        for i, state in enumerate(self.states):

            printProgressBar(
                i, len(self.states), prefix="Finalize:", suffix="Complete", length=50
            )
            state.finalize()

        print("\n")

    def save(self, name: str = "ats"):

        filehandler = open(f"data/{name}.pkl", "wb")
        pickle.dump(self, filehandler)
