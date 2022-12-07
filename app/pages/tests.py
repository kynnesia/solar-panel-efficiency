from weather_prepro import weather_df, aggregates_df, monthly_pvwatts_data, monthly_weather_df
#from aggregate import monthly_df_to_model, general_monthly_df
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

if __name__ == "__main__":
    print(aggregates_df(weather_df(40.4637,3.7492)))
