import pandas as pd
import requests
import pathlib


# For option 1
def weather_df(lat:float,
              lon:float,
              year:int=2017, # "YYYY"
              )-> pd.DataFrame:
    """
    Given a latitude, longitude, start date, and end date, provide
    a daily dataframe of all features.
    """
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-30"
    weather_url = 'https://archive-api.open-meteo.com/v1/era5'
    weather_params = {
      "latitude" : lat,
      "longitude" : lon,
      "start_date" : start_date,
      "end_date" : end_date,
      "timezone" : "Europe/Madrid",
      "daily" : ["temperature_2m_max",
                  "temperature_2m_min",
                  "precipitation_sum",
                  "rain_sum",
                  "snowfall_sum",
                  "precipitation_hours",
                  "sunrise",
                  "sunset",
                  "windspeed_10m_max",
                  "windgusts_10m_max",
                  "winddirection_10m_dominant",
                  "shortwave_radiation_sum", # ! IMPORTANT METRIC
                  "et0_fao_evapotranspiration"]
    }
    weather_data = requests.get(weather_url, params=weather_params)
    weather_dict = weather_data.json()
    weather_df = pd.DataFrame(weather_dict["daily"])
    weather_df["latitude"] = lat
    weather_df["longitude"] = lon
    weather_df["timestamp"] = year
    return weather_df

# For Option 1
def aggregates_df(weather_df:pd.DataFrame) -> pd.DataFrame:
    """
    This function aggregates all the rows by summing or averaging them.
    """
    # To Datetime
    #weather_df["sunrise"] = pd.to_datetime(weather_df["sunrise"])
    #weather_df["sunset"] = pd.to_datetime(weather_df["sunset"])
    weather_df.drop("time", axis=1, inplace=True)

    # Aggregates
    max_temp = weather_df["temperature_2m_max"].mean()
    min_temp = weather_df["temperature_2m_min"].mean()
    prec_sum = weather_df["precipitation_sum"].sum()
    rain_sum = weather_df["rain_sum"].sum()
    snow_sum = weather_df["snowfall_sum"].sum()
    prec_hours = weather_df["precipitation_hours"].sum()
    sun_hours = (weather_df["sunset"] - weather_df["sunrise"]).mean()
    wind_speed_max = weather_df["windspeed_10m_max"].mean()
    wing_gusts_max = weather_df["windgusts_10m_max"].mean()
    wind_direction = weather_df["winddirection_10m_dominant"].mean()
    solar_radiation = weather_df["shortwave_radiation_sum"].sum()
    evapotransp = weather_df["et0_fao_evapotranspiration"].sum()

    # List
    aggregates = pd.DataFrame([weather_df["timestamp"].iat[0],
                       weather_df["latitude"].iat[0],
                       weather_df["longitude"].iat[0],
                       max_temp, min_temp, prec_sum, rain_sum, snow_sum,
                       prec_hours, wind_speed_max, wing_gusts_max,
                       wind_direction, solar_radiation, evapotransp]).T
    aggregates.columns = ["Timestamp", "Latitude","Longitude","Maximum Temp.",
                          "Minimum Temp.","Precipitation","Rain","Snow",
                          "Precipitation hours","Maximum Wind Speed",
                          "Maximum Wing Gusts","Wind Direction","Solar Radiation",
                          "Evapotransp."]
    # Return
    return aggregates


def monthly_weather_df(lat:float,
              lon:float,
              year:int, # "YYYY"
              )-> pd.DataFrame:
    """
    Given a latitude, longitude, start date, and end date, provide
    a daily dataframe of all features.
    """
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-30"
    weather_url = 'https://archive-api.open-meteo.com/v1/era5'
    weather_params = {
      "latitude" : lat,
      "longitude" : lon,
      "start_date" : start_date,
      "end_date" : end_date,
      "timezone" : "Europe/Madrid",
      "daily" : ["temperature_2m_max",
                  "temperature_2m_min",
                  "precipitation_sum",
                  "rain_sum",
                  "snowfall_sum",
                  "precipitation_hours",
                  "sunrise",
                  "sunset",
                  "windspeed_10m_max",
                  "windgusts_10m_max",
                  "winddirection_10m_dominant",
                  "shortwave_radiation_sum", # ! IMPORTANT METRIC
                  "et0_fao_evapotranspiration"]
    }
    weather_data = requests.get(weather_url, params=weather_params)
    weather_dict = weather_data.json()
    weather_df = pd.DataFrame(weather_dict["daily"])
    weather_df["timestamp"] = year
    weather_df["month"] = weather_df["time"].str[5:7]

    output = weather_df.groupby(by="month").agg("mean")
    output["latitude"] = lat
    output["longitude"] = lon
    return output



def monthly_pvwatts_data(lat,
                         lon):
                         #proxy,
                         #timeout=5):
    url = 'https://developer.nrel.gov/api/pvwatts/v6.json?api_key=IAwRTEmh1TANaK6K6IwN65trPMdCydwXB0lPcg6f'
    params = {"lat":lat,
              "lon":lon,
              "system_capacity":4,
              "azimuth":180,
              "tilt":40,
              "array_type":1,
              "losses":10,
              "module_type":1,
              "radius":0,
              "dataset":"intl"}
    technical_data = requests.get(url, params=params)
    response = technical_data.json().get("outputs")
    altitude = technical_data.json().get("station_info").get("elev")
    #ac = response.get("ac_annual")
    solrad = response.get("solrad_annual")
    df = pd.DataFrame([altitude,solrad,lat,lon]).T
    df.columns=["Altitude","Solar Radiation","Latitude","Longitude"]
    return df
