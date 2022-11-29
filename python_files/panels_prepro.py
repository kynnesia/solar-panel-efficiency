
import pandas as pd
import seaborn as sns
import pandas as pd

def get_dataframe_option1() :
    df = pd.read_csv("data/global_power_plant_database.csv", low_memory=False)
    df = df[df['primary_fuel'] == 'Solar'].reset_index(drop=True)
    df.drop(columns=['gppd_idnr', 'capacity_mw','other_fuel1', 'other_fuel2', 'other_fuel3', 'commissioning_year', 'owner', 'source', 'url',
       'geolocation_source', 'wepp_id', 'year_of_capacity_data',
       'generation_gwh_2013', 'generation_gwh_2014', 'generation_gwh_2015',
       'generation_gwh_2016', 'generation_gwh_2017', 'generation_gwh_2018',
       'generation_gwh_2019', 'generation_data_source',
       'estimated_generation_gwh_2013', 'estimated_generation_gwh_2014',
       'estimated_generation_gwh_2015', 'estimated_generation_gwh_2016',
       'estimated_generation_gwh_2017', 'estimated_generation_note_2013',
       'estimated_generation_note_2014', 'estimated_generation_note_2015',
       'estimated_generation_note_2016', 'estimated_generation_note_2017'], inplace=True)
    return df
