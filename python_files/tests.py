from weather_prepro import weather_df, aggregates_df
from panels_prepro import get_dataframe_option3, get_dataframe_option1
from aggregate import df_to_model
from api_sourcing import get_data
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == "__main__":
    get_data(45.2,2.1,)
