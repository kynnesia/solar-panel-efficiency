import pandas as pd

data_graph = pd.read_csv('raw_data/global_power_plant_database.csv')

#dropping NaN

def get_lat_lon ():
    return data_graph[['latitude','longitude']]