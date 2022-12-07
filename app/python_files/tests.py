from weather_prepro import weather_df, aggregates_df, monthly_pvwatts_data, monthly_weather_df
#from aggregate import monthly_df_to_model, general_monthly_df
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

if __name__ == "__main__":
    def strdate_to_float(column:pd.Series) -> pd.Series:
        column = column.astype(str)
        column = column.str.lstrip("0").str.strip(" days").str[0:8]
        new_column = (column.str[:2]).astype(float)*60 + (column.str[3:5]).astype(float) + (column.str[6:8]).astype(float)/60
        return new_column
    df = aggregates_df(weather_df(40.4637,3.7492))
    df["Sun Hours"] = strdate_to_float(df["Sun Hours"])
    print(df)
