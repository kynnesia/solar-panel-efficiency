from weather_prepro import weather_df, aggregates_df
from panels_prepro import get_dataframe_option1
from aggregate import panels_weather_dict
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == "__main__":
    df = get_dataframe_option1()
    panels_weather_dict(df, 2017).to_csv('2017_panels_weather_2.csv',index=False)
