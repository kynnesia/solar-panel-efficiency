from weather_prepro import weather_df, aggregates_df, monthly_pvwatts_data, monthly_weather_df
from panels_prepro import get_dataframe_option3, get_dataframe_option1
from aggregate import monthly_df_to_model, general_monthly_df, general_yearly_df
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

if __name__ == "__main__":
    df = pd.read_csv("raw_data/listado-longitud-latitud-municipios-espana.csv",
                     encoding_errors="replace")
    general_yearly_df(df,2017,supervised=False).to_csv("data_SPAIN/SPAIN_yearly_2017_weather_metrics.csv")
