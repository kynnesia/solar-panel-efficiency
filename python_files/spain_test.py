from weather_prepro import weather_df, aggregates_df, monthly_pvwatts_data, monthly_weather_df
from panels_prepro import get_dataframe_option3, get_dataframe_option1
from aggregate import monthly_df_to_model
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

if __name__ == "__main__":
    # proxies
    df = pd.read_csv("data/listado-longitud-latitud-municipios-espana.csv")
    monthly_df_to_model(df).to_csv("data_SPAIN/SPAIN_monthly_2017_target_metrics.csv")
