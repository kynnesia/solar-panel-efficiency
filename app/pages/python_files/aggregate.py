from panels_prepro import get_dataframe_option1
from weather_prepro import weather_df,monthly_weather_df, aggregates_df, monthly_pvwatts_data
import pandas as pd
import numpy as np
import time
from itertools import cycle
from termcolor import colored
import logging
#from sklearn.pipeline import make_pipeline
#from sklearn.preprocessing import MinMaxScaler

# Yearly general weather conditions
def general_yearly_df(df:pd.DataFrame,
                        year:int,
                        supervised:bool) -> pd.DataFrame:
    """
    Scrapes yearly general weather conditions for each lat-lon
    """
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
        for y in range(1):
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

# Monthly general weather conditions
def general_monthly_df(df:pd.DataFrame,
                        year:int,
                        ) -> pd.DataFrame:
    """
    Scrapes yearly general weather conditions for each lat-lon
    """
    data = pd.DataFrame()
    last_succesful_index = 0
    for idx , row in df.iloc[last_succesful_index:].iterrows():
        lat = row["latitude"]
        lon = row["longitude"]
        print("*"*50 + f"\n ITERATION={idx+1}| Fetching data for lat={lat:.2f},lon={lon:.2f}")
        try:
            ##send HTTP request
            new_data = monthly_weather_df(lat=lat,lon=lon,year=year)

            ##store data
            new_data["latitude"] = lat
            new_data["longitude"] = lon
            data = pd.concat([data, new_data], axis=0)
            print(f"🤑 Row added !")
        except:
            time.sleep(5)
            continue
    return data


# (proxies) Monthly technical weather conditions
def monthly_df_to_model(df:pd.DataFrame):
    """
    Scrapes monthly technical features for each latitude-longitude
    """
    # PROXIES
    proxies = ['208.82.61.66:3128',
    '134.238.252.143:8080',
    '75.126.253.8:8080',
    '178.63.237.147:8080',
    '46.105.178.147:3128',
    '44.204.196.8:3128']

    prox_gen = cycle(proxies)

    # ALL DATA
    data = pd.DataFrame()


    last_succesful_index = 0
    count = 0
    for idx , row in df.iloc[last_succesful_index:].iterrows():
        lat = row["latitude"]
        lon = row["longitude"]
        print("*"*50 + f"\n ITERATION={idx+1}| Fetching data for lat={lat:.2f},lon={lon:.2f}")
        print(f"💭 Computing {count}/{df.shape[0]} row.")
        #start by using proxies one-by-one until one succeeds
        ## we start by using proxy one
        failures = 0
        for proxy in prox_gen:
            print(f"Attempting sourcing with proxy {proxy}...")
            try:
                ##send HTTP request
                new_data = monthly_pvwatts_data(lat,lon,proxy)

                ##store data
                new_data["latitude"] = lat
                new_data["longitude"] = lon
                data = pd.concat([data, new_data], axis=0)
                print(f"🤑 Row added !")
                count =+1
                ##break the infinite loop and continue to next (x,y)
                break
            except Exception as e:
                print(colored(f"PROXY FAILED!","red"))
                ##counting failed attempts
                failures += 1
                print(colored(f"TOTAL FAILURES={failures}!"))

                ##if we tried all proxies and none succeeded break loop
                ##and terminate
                if failures == len(proxies):
                    break
                ##else retry with another proxy
                else:
                    print("RETRYING...")
                    continue

    return data
