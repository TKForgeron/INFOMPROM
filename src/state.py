from src.bucket import Bucket
from src.bucket_preprocessor import Preprocessor


class State:
    def __init__(
        self,
        id,
        activities: list[str],
        representation: str,
        y_col: str,
        encoding_operation: str = None,
        model_type: str = None,
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
        self.bucket = Bucket(y_col, [], encoding_operation, model_type, seed, cv)
        self.subsequent_states = []

    def add_event(self, row: dict):

        self.bucket.append(row)
        # pass

    def add_subseq_state(self, state_id):

        self.subsequent_states.append(state_id)

    def equals_state(self, activities):

        return self.activities == activities

    def predict(self, event) -> float:

        pp = Preprocessor(
            self.bucket.preprocessor.y_col, self.bucket.preprocessor.encoding_operation
        )
        event = pp.prepare_for_prediction(event, self.bucket.x_cols)

        print(f"Predicting remaining time using {self.bucket.model} model...")
        y_pred = self.bucket.predict_one(event)

        return y_pred
        # print(
        #     f"PREDICT -> INCIDENT: {event['Incident ID']} in STATE ID: {self.id}\n-- PE: {event['PrevEvents']}"
        # )

        # return 1  # placeholder value

    def finalize(self):

        self.bucket.finalize()
        # pass
        # print(f"Some method that prepares the state {self.id} bucket for prediction")
