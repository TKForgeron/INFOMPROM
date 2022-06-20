import sys
import pandas as pd
from src.state import State
from src.helper import print_progress_bar
import pickle
import datetime





class ATS:
    def __init__(
        self,
        trace_id_col: str,
        act_col: str,
        y_col: str,
        model,
        representation: str = "trace",
        horizon: int = sys.maxsize, #infite
        filter_out: list = [],
        seed: int = 42,
        cv: int = 5,
    ) -> None:

        print("START CREATING ATS")

        self.trace_id_col = trace_id_col
        self.act_col = act_col
        self.y_col = y_col


        self.rep = representation
        self.horizon = horizon
        self.filter_out = filter_out

        self.model = model


        self.seed = seed
        self.cv = cv

        self.finalized = 0

        empty_state = State(
            0,
            [],
            representation,
            self.y_col,
            model,
            seed,
            cv,
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
                id=state_id,
                activities=activities,
                representation=self.rep,
                y_col=self.y_col,
                model=self.model,
                seed=self.seed,
                cv=self.cv
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

        grouped = pd.concat([X, y], axis=1).groupby(self.trace_id_col)

        length = len(grouped)
        i = 0

        print_progress_bar(0, length, prefix="Create:", suffix="Complete", length=50)
        for name, group in grouped:
            
            y = group.pop(self.y_col).tolist()
            X = group.to_dict("records")
            
            # self.add_trace(group.to_dict("records"))
            self.add_trace(X, y)

            print_progress_bar(
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

            print_progress_bar(
                0, len(self.states), prefix="Print:", suffix="Complete", length=50
            )

            print(f"Output file created on: {datetime.datetime.now()}", file=text_file)

            for i, state in enumerate(self.states):

                print_progress_bar(
                    i+1, len(self.states), prefix="Print:", suffix="Complete", length=50
                )
                print(f"id: {state.id}", file=text_file)
                print(f"activities: {state.activities}", file=text_file)

                print(f"Subseq: {state.subsequent_states}", file=text_file)

                print("Data:", file=text_file)

                if self.finalized == 0:
                    for row in state.bucket.X:

                        print(row, file=text_file)
                else:
                    print(state.bucket.X, file=text_file)
                    print(state.bucket.y, file=text_file)

                print("\n--------------------------------------\n", file=text_file)

        print("\n")  # some weird bug in the progress bar

    def predict(self, event: dict) -> float:

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

    def finalize(self, progress_bar=True) -> None:
        """
        This function finalizes the ATS such that can work as
        a prediction model.

        """

        self.finalized = 1

        if progress_bar:
            print_progress_bar(
                0, len(self.states), prefix="Finalize:", suffix="Complete", length=50
            )

        for i, state in enumerate(self.states):
            
            if progress_bar:
                print_progress_bar(
                    i+1, len(self.states), prefix="Finalize:", suffix="Complete", length=50
                )
            state.finalize()

        if progress_bar:

            print("\n")

    def save(self, name: str = "ats"):

        filehandler = open(f"data/{name}.pkl", "wb")
        pickle.dump(self, filehandler)
