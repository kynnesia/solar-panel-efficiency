from weather_prepro import weather_df, aggregates_df, monthly_pvwatts_data, monthly_weather_df
#from aggregate import monthly_df_to_model, general_monthly_df
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

if __name__ == "__main__":
    df = pd.read_csv('data_prediction.csv')
    print(np.exp(df["production prediction"]).mean())
