from src.bucket import Bucket
from src.representation import Representation
from dataclasses import dataclass, field


@dataclass(slots=True)
class State:
    id: int
    activities: list[str]
    representation: Representation
    y_col: str
    cols_to_drop: list[str]
    seed: int
    cv: int
    bucket: Bucket = field(init=False)
    subsequent_states: list = field(default_factory=list)

    def __post_init__(self):
        self.bucket = Bucket(
            y_col=self.y_col, cols_to_drop=self.cols_to_drop, seed=self.seed, cv=self.cv
        )

    def add_event(self, row: dict, y_val: int):
        self.bucket.append(row, y_val=y_val)

    def add_subseq_state(self, state_id):
        self.subsequent_states.append(state_id)

    def equals_state(self, activities):
        return self.activities == activities

    def predict(self, event) -> float:
        return self.bucket.predict_one(event)

    def finalize(self, model):
        self.bucket.finalize(model)
