import sys
import pandas as pd
from src.state import State
from src.helper import print_progress_bar
from src.representation import Representation
import pickle
import datetime
from typing import Any


class ATS:
    def __init__(
        self,
        case_id_col: str,
        act_col: str,
        y_col: str,
        representation: Representation = Representation.TRACE,
        horizon: int = sys.maxsize,  # infite
        filter_out: list = [],
        seed: int = 42,
        cv: int = 5,
    ) -> None:

        print("START CREATING ATS")

        self.case_id_col: str = case_id_col
        self.act_col: str = act_col
        self.y_col: str = y_col

        self.representation: Representation = representation
        self.horizon: int = horizon
        self.filter_out: list = filter_out

        self.seed: int = seed
        self.cv: int = cv

        self.finalized: bool = False

        empty_state: State = State(
            0,
            [],
            representation,
            self.y_col,
            [case_id_col, act_col],
            seed,
            cv,
        )
        self.states: list[State] = [empty_state]
        self.model: Any = None

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
                id=state_id,
                activities=activities,
                representation=self.representation,
                # under here are the Bucket parameters
                y_col=self.y_col,
                cols_to_drop=[self.case_id_col, self.act_col],
                seed=self.seed,
                cv=self.cv,
            )
        )

        return state_id

    def transform_rep(self, act: list[str]) -> list[str]:

        # filtering | TODO: we might want to do this for the trace once using pd.filter()
        act = [x for x in act if x not in self.filter_out]

        # horizon
        act = act[-self.horizon :]

        # representation
        if self.representation == Representation.SET:
            act = sorted(list(set(act)))
        elif self.representation == Representation.MULTISET:
            act = sorted(act)

        return act.copy()

    def add_trace(self, trace: list[dict], y_vals) -> None:
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
        curr_state.add_event(trace[0], y_vals[0])

        # act = []
        for i, event in enumerate(trace):

            y_val = y_vals[i]

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

                curr_state.add_subseq_state(state_id)

            curr_state = self.states[next_state_id]

            curr_state.add_event(event, y_val)

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """
        Main function that creates the ATS given an event log.

        Parameters
        ----------
            df : pd.Dataframe
                The event log
        """

        self.x_cols = X.columns.tolist()
        self.y_col = y.name

        grouped = pd.concat([X, y], axis=1).groupby(self.case_id_col)

        length = len(grouped)
        i = 0

        print_progress_bar(0, length, prefix="Fit:", suffix="Complete", length=50)
        for name, group in grouped:

            y = group.pop(self.y_col).tolist()  # TODO: let y be pd.Series
            X = group.to_dict("records")  # TODO: let X be pd.DataFrame

            self.add_trace(X, y)

            print_progress_bar(
                i + 1, length, prefix="Fit:", suffix="Complete", length=50
            )
            i += 1

        print("\n")

    def print(self) -> None:  # would call to_txt()
        """

        Function that prints the (Annotated) Transition System to
        a TXT file. Right now, merely for debugging purposes.

        """

        with open("data/ATS_output.txt", "w") as text_file:

            print_progress_bar(
                0, len(self.states), prefix="Print:", suffix="Complete", length=50
            )

            print(f"Output file created on: {datetime.datetime.now()}", file=text_file)

            for i, state in enumerate(self.states):

                print_progress_bar(
                    i + 1,
                    len(self.states),
                    prefix="Print:",
                    suffix="Complete",
                    length=50,
                )
                print(f"id: {state.id}", file=text_file)
                print(f"activities: {state.activities}", file=text_file)

                print(f"Subseq: {state.subsequent_states}", file=text_file)

                print("Data:", file=text_file)

                if not self.finalized:
                    for row in state.bucket.X:

                        print(row, file=text_file)
                else:
                    print(state.bucket.X, file=text_file)
                    print(state.bucket.y, file=text_file)

                print("\n--------------------------------------\n", file=text_file)

        print("\n")  # some weird bug in the progress bar

    def predict_one(self, event: dict) -> float:
        """

        Function that traverses the ATS to find the bucket that must
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

        if self.finalized:
            search_term = []
            state = self.states[0]
            state_id = 0

            for l in range(1, len(event["PrevEvents"]) + 1):

                sub_seq = state.subsequent_states

                search_term = event["PrevEvents"][:l]
                search_term = self.transform_rep(search_term)

                next_state = 0

                for s in sub_seq:
                    if self.states[s].activities == search_term:
                        state = self.states[s]
                        state_id = s
                        next_state = 1
                        break

                if event["PrevEvents"] == state.activities or next_state == 0:

                    return state.predict(event)

            return state.predict(event)
        else:
            raise RuntimeError(
                "The ATS was not yet finalized. Do this first before running ATS.predict_one()"
            )

    def finalize(self, model, progress_bar: bool = True) -> None:
        """This function finalizes the ATS by giving each bucket a model to predict with."""

        self.model = model
        self.finalized = True

        if progress_bar:
            print_progress_bar(
                0, len(self.states), prefix="Finalize:", suffix="Complete", length=50
            )

        for i, state in enumerate(self.states):

            if progress_bar:
                print_progress_bar(
                    i + 1,
                    len(self.states),
                    prefix="Finalize:",
                    suffix="Complete",
                    length=50,
                )
            state.finalize(model)

        if progress_bar:

            print("\n")

    def definalize(self) -> None:
        self.model = None
        self.finalized = False

    def save(self, name: str = "ats", dir: str = "./data") -> str:
        file = f"{dir}/{name}.pkl"
        filehandler = open(file, "wb")
        pickle.dump(self, filehandler)

        return file
