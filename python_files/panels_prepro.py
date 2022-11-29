
import pandas as pd
import seaborn as sns
import pandas as pd
import os

data_path = os.environ.get("PATH_SOLAR_PANEL_DB")

def get_dataframe_option1() :
    df = pd.read_csv(data_path, low_memory=False)
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



def get_dataframe_option2() :
    df = pd.read_csv(data_path, low_memory=False)
    df = df.dropna(subset=['estimated_generation_gwh_2017'])
    df = df[df['primary_fuel']== 'Solar'].reset_index(drop=True)
    df.drop(columns=['gppd_idnr', 'capacity_mw','other_fuel1', 'other_fuel2', 'other_fuel3', 'commissioning_year', 'owner', 'source', 'url',
       'geolocation_source', 'wepp_id', 'year_of_capacity_data',
       'generation_gwh_2013', 'generation_gwh_2014', 'generation_gwh_2015',
       'generation_gwh_2016', 'generation_gwh_2017', 'generation_gwh_2018','generation_gwh_2019',
        'generation_data_source',
       'estimated_generation_gwh_2013', 'estimated_generation_gwh_2014',
       'estimated_generation_gwh_2015', 'estimated_generation_gwh_2016', 'estimated_generation_note_2013',
       'estimated_generation_note_2014', 'estimated_generation_note_2015',
       'estimated_generation_note_2016', 'estimated_generation_note_2017'], inplace=True)
    return df


# 3. Dataframe option 3
# all the plants
# estimation for all the years (2013, 2014, 2015, 2016, 2017)
# real production for the years(2018, 2019)


def get_dataframe_option3 () :
    df = pd.read_csv(data_path, low_memory=False)
    df.drop(columns=['gppd_idnr', 'capacity_mw',
        'other_fuel1', 'other_fuel2',
        'other_fuel3', 'commissioning_year', 'owner', 'source', 'url',
        'geolocation_source', 'wepp_id', 'year_of_capacity_data',
        'generation_gwh_2013', 'generation_gwh_2014', 'generation_gwh_2015',
        'generation_gwh_2016', 'generation_gwh_2017','generation_data_source',
        'estimated_generation_note_2013','estimated_generation_note_2014', 'estimated_generation_note_2015',
        'estimated_generation_note_2016', 'estimated_generation_note_2017'], inplace=True)
    df = df[df['primary_fuel']== 'Solar'].reset_index(drop=True)
    df = pd.melt(df, id_vars=['country', 'country_long', 'name', 'latitude', 'longitude',
        'primary_fuel'], value_vars=['generation_gwh_2018', 'generation_gwh_2019',
        'estimated_generation_gwh_2013', 'estimated_generation_gwh_2014',
        'estimated_generation_gwh_2015', 'estimated_generation_gwh_2016',
        'estimated_generation_gwh_2017'], var_name='year', value_name='production')
    df['year'] = df['year'].str.strip('generation_gwh_').str.strip('estimated_generation_gwh_')
    df = df.dropna(subset=['production']).reset_index(drop=True)
    return df
