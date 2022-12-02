from weather_prepro import weather_df, aggregates_df
from panels_prepro import get_dataframe_option3, get_dataframe_option1
from aggregate import df_to_model
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == "__main__":
    # UNSUPERVISED MODEL WITH 5 YEARS
    df_unsup = get_dataframe_option1()
    (df_to_model(df_unsup,2015, supervised=False)).to_csv("10y_unsupervised_df.csv")
    print("--------------COMPLETED UNSUPERVISED MODEL ----------------")
