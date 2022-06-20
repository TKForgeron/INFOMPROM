from src.bucket import Bucket
from src.bucket_preprocessor import Preprocessor


class State:
    def __init__(
        self,
        id,
        activities: list[str],
        representation: str,
        x_cols: list[str],
        y_col: str,
        model,
        encoding_operation: str = None,
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
            id=id,
            x_cols=x_cols,
            y_col=y_col,
            data=[],  # is empty as we fill this on-the-go and transform to pd.DataFrame upon completion
            encoding_operation=encoding_operation,
            model=model,
            seed=seed,
            cv=cv,
        )
        self.subsequent_states = []

    def add_event(self, row: dict):

        self.bucket.append(row)

    def add_subseq_state(self, state_id):

        self.subsequent_states.append(state_id)

    def equals_state(self, activities):

        return self.activities == activities

    def predict(self, event) -> float:

        # MOET NOG VERANDEREN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        print(f"Predicting remaining time using {self.bucket.model} model")
        y_pred = self.bucket.predict_one(event)

        # dit is wat we zometeen moeten runnen en dan kunnen we kijken of het overeen komt met de avg in de ats_output.txt
        print(f"state {self.id} predicts: {y_pred}")
        return y_pred
        # print(
        #     f"PREDICT -> INCIDENT: {event['Incident ID']} in STATE ID: {self.id}\n-- PE: {event['PrevEvents']}"
        # )

    def finalize(self):

        self.bucket.finalize()
        # pass
        # print(f"Some method that prepares the state {self.id} bucket for prediction")
