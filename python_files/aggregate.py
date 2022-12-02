from panels_prepro import get_dataframe_option1
from weather_prepro import weather_df, aggregates_df
import pandas as pd
import numpy as np
import time
#from sklearn.pipeline import make_pipeline
#from sklearn.preprocessing import MinMaxScaler

def df_to_model(df:pd.DataFrame,
                        year:int,
                        supervised:bool) -> pd.DataFrame:
    if supervised == False:
        dict_ ={'year': [],
                'latitude': [],
                'longitude': [],
                'temperature_2m_max': [],
                'temperature_2m_min': [],
                'precipitation_sum': [],
                'rain_sum': [],
                'snowfall_sum': [],
                'precipitation_hours': [],
                'sun hours':[],
                'windspeed_10m_max':[],
                'windgusts_10m_max':[],
                'winddirection_10m_dominant':[],
                'shortwave_radiation_sum':[],
                'et0_fao_evapotranspiration':[]
                }
        for y in range(5):
            print(f"Year {year+y}")
            loading=1
            for i, r in df.iterrows():
                try:
                    print(f"💭 Computing {loading}/{df.shape[0]} row.")

                    latitude = r["latitude"]
                    longitude = r["longitude"]

                    list_ = aggregates_df(weather_df(lat=latitude,
                                                        lon=longitude,
                                                        year=year+y))
                    count = 0
                    for k,v in dict_.items():
                        dict_[k].append(list_[count])
                        count +=1

                    loading +=1
                except:
                    time.sleep(5)
                    continue
        return pd.DataFrame(dict_)


    if supervised == True:
        dict_ ={'year':[],
                'latitude': [],
                'longitude': [],
                'temperature_2m_max': [],
                'temperature_2m_min': [],
                'precipitation_sum': [],
                'rain_sum': [],
                'snowfall_sum': [],
                'precipitation_hours': [],
                'sun hours':[],
                'windspeed_10m_max':[],
                'windgusts_10m_max':[],
                'winddirection_10m_dominant':[],
                'shortwave_radiation_sum':[],
                'et0_fao_evapotranspiration':[],
                'production':[]
                }
        loading=1
        for i, r in df.iterrows():
            try:
                print(f"💭 Computing {loading}/{df.shape[0]} row.")

                latitude = r["latitude"]
                longitude = r["longitude"]
                target = r[-1]

                list_ = aggregates_df(weather_df(lat=latitude,
                                                lon=longitude,
                                                year=r["year"])) # ! CAUTION
                list_.append(target)
                count = 0
                for k,v in dict_.items():
                    dict_[k].append(list_[count])
                    count +=1
                loading +=1
            except:
                time.sleep(5)
                continue
        return pd.DataFrame(dict_)

    else:
        print("Supervised or Unsupervised not specified.")
        return KeyError
