from src.bucket import Bucket
import pandas as pd

df = pd.read_csv("data/converted_df.csv", index_col=0)

col_index_no = df.columns.get_loc("horse")
print(col_index_no)

b = Bucket(y_col="RemainingTime", data=df)

data = b.data
b.encode()
X, y = b._generate_split()

b.model.fit(X, y)
