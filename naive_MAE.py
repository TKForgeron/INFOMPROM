

# MAE calculation


from src.input_data import InputData


PREPROCESSING_IN_FILE = "incidentProcess_custom.csv"

input = InputData(PREPROCESSING_IN_FILE)

input.calculate_naive_MAE()

input.save_df()

print(f"MAE time: {input.df['AE_time_days'].mean()}")
print(f"MAE activties: {input.df['AE_activities'].mean()}")