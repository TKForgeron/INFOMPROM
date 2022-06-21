from src.bucket import Bucket


class State:
    def __init__(
        self,
        id,
        activities: list[str],
        representation: str,
        y_col: str,
        model,
        seed: int = None,
        cv: int = None,
    ) -> None:
        """
        Constructs a new State object.

        Parameters
        ----------
            activities : [str]
                The activities that make up the state.
        """

        self.activities = activities
        self.rep = representation
        self.id = id
        self.bucket = Bucket(
            y_col=y_col,
            model=model,
            seed=seed,
            cv=cv,
        )
        self.subsequent_states = []

    def add_event(self, row: dict, y_val: int):

        self.bucket.append(row, y_val=y_val)

    def add_subseq_state(self, state_id):

        self.subsequent_states.append(state_id)

    def equals_state(self, activities):

        return self.activities == activities

    def predict(self, event) -> float:

        # MOET NOG VERANDEREN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        print(f"Predicting remaining time using {self.bucket.model} model")
        y_pred = self.bucket.predict_one(event)

        # print(f"state {self.id} predicts: {y_pred / (60*60)} hour")
        return y_pred

    def finalize(self):

        self.bucket.finalize()
        # print(f"Some method that prepares the state {self.id} bucket for prediction")
