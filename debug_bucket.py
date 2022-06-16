from src.bucket import Bucket
from src.preprocessor import Preprocessor
import pandas as pd

df = pd.read_csv("data/converted_df.csv")

three_traces = df.iloc[:, :73]
x_pred = df.iloc[74:75]

bucket = Bucket(y_col="RemainingTime", data=three_traces, model_type="median")
bucket.finalize()

pp = Preprocessor(
    y_col=bucket.preprocessor.y_col,
    encoding_operation=bucket.preprocessor.encoding_operation,
)
three_traces = pp.prepare_for_prediction(three_traces, bucket.x_cols)

# log = three_traces[bucket.x_cols]
# print("-" * 10)
# print(log)
# print("-" * 10)

print(f"Predicting remaining time using {bucket.model} model...")
y_pred = bucket.model.predict(three_traces)
print(f"Example of first 5 predictions: {y_pred[:5]}")
