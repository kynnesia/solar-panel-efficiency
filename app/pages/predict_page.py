import streamlit as st
import folium
import streamlit as st
from folium.plugins import Draw
import requests
from streamlit_folium import st_folium
import math
from app.python_files.weather_prepro import weather_df, aggregates_df

st.set_page_config(layout="wide")

#------- TITLE -------
st.markdown("""
    # Which is the best place to set up a Solar Panel Station?
    """)
st.markdown("""
    ## On stream predictions of solar energy production through Spain
    """)

#------- MARKDOWN -------
st.markdown("This project includes an on-stream prediction API. This allows\
    the web user to choose a point from a map. Then, the API stores the latitude\
    and longitude of that exact point. With that, scrapes the chosen features\
    of that position (temperature, wind speed, solar radiation, altitude, etc.)\
    . With the features stored, and with a trained model, is able to predict\
    the energy produced at that specific point if there was an average-size solar\
    station.")


#------- INTERACTIVE MAP -------
m = folium.Map(location=[40.396764,-3.735352], zoom_start=6)
Draw(export=True).add_to(m)

output = st_folium(m, width=1000, height=500)

bounds = output['bounds']
if output.get("last_active_drawing") != None:
    st.write(output.get("last_active_drawing").get("geometry").get("coordinates"))
    lat = output.get("last_active_drawing").get("geometry").get("coordinates")[0]
    lng = output.get("last_active_drawing").get("geometry").get("coordinates")[1]
    st.dataframe(aggregates_df(weather_df(lat,lng)))

URL = 'https://api.ohsome.org/v1/elements/count/density'

#lat = output['center']['lat']
#lon = output['center']['lng']
#rad = (output.get('last_circle_radius'))
#data = {"bcircles": f"{lon},{lat},{rad}", "format": "json", "time": "2022-05-07", "filter": "landuse=industrial"}
#st.write(data)
#response = requests.post(URL, data=data)
#st.write(response.json())
