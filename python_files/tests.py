from weather_prepro import weather_df, aggregates_df, monthly_pvwatts_data, monthly_weather_df
from panels_prepro import get_dataframe_option3, get_dataframe_option1
from aggregate import df_to_model, add_target
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

if __name__ == "__main__":
    proxies = ['208.82.61.66:3128',
    '134.238.252.143:8080',
    '75.126.253.8:8080',
    '178.63.237.147:8080',
    '46.105.178.147:3128',
    '44.204.196.8:3128']
    print((monthly_pvwatts_data(45.2,2.1,"208.82.61.66:3128")))
