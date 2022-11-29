from weather_prepro import weather_df, aggregates_df
from panels_prepro import get_dataframe_option3, get_dataframe_option1
from aggregate import df_to_model
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == "__main__":
    # SUPERVISED MODEL WITH 1+ YEAR
    #df_sup = get_dataframe_option3()
    #(df_to_model(df_sup,0,supervised=True)).to_csv("allyears_supervised_df.csv")

    # UNSUPERVISED MODEL WITH 5 YEARS
    #df_unsup = get_dataframe_option1().head(20)
    #(df_to_model(df_unsup,2015, supervised=False)).to_csv("10y_unsupervised_df.csv")
