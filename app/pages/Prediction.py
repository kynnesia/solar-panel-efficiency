import streamlit as st
import folium
import streamlit as st
from folium.plugins import Draw
import requests
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
import math
import pandas as pd
from python_files.weather_prepro import weather_df, aggregates_df, monthly_pvwatts_data

html = '''
    <style>
    .Prediction {
        color=red
    }
    </style>
'''

pred_df = pd.read_csv('app/pages/raw_data/production_predicted_with_cities.csv')
pred_df = pred_df[pred_df["production prediction"]<200]
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
m = folium.Map(location=[40.396764,-3.735352], zoom_start=3)
Draw(export=True).add_to(m)

output = st_folium(m, width=1000, height=500)

bounds = output['bounds']
if output.get("last_active_drawing") != None:
    lat = output.get("last_active_drawing").get("geometry").get("coordinates")[0]
    lng = output.get("last_active_drawing").get("geometry").get("coordinates")[1]
    c1,c2,c3 = st.columns(3)
    c1.metric("Latitude",round(lat,3))
    c2.metric("Longitude",round(lng,3))
    if c3.button('Predict'):
        weather = aggregates_df(weather_df(lat,lng))
        tech = monthly_pvwatts_data(lat,lng)
        df = weather.merge(tech, on=["latitude","longitude"], how="left")
        dict_ = df.to_dict(orient="records")[0]
        url = "https://solar-gtumit4j3a-ew.a.run.app/predict"
        response = requests.get(url, params=dict_)
        prediction = response.json().get("prediction")
        #st.metric("Prediction (GWh)",round(prediction,2))
        c2.title(f"Prediction: {round(prediction,2)} GWh")
        c2.write(f"With this prediction, and considering an average energy \
            spenditure of 7.95MWh/year per habitant, the average-sized solar station at \
            this location would fulfill the yearly demand of **{int(prediction/(7.95/1_000))}**\
            citizens.")
        c2.write(f"That would be **{round(prediction/13_222*100,1)} %** of energy consumed in \
            Barcelona.")
        if prediction > 15.14:
            c2.write(f"15.14GWh/year is the average energy production of all stations. \
                If a standard solar station was placed in this location, it would produce \
                **{round((prediction - 15.14)/15.14,1)}%** more than the average, so it would be a suitable place \
                for a solar station.")
        else:
            c2.write(f"15.14GWh/year is the average energy production of all stations. \
            If a standard solar station was placed in this location, it would produce \
            **{round((prediction - 15.14)/15.14,1)}%** less than the average, so would not be a suitable place \
            for a solar station.")
        fig = px.box(pred_df, y="production prediction")
        fig.add_trace(go.Scatter(y=prediction), mode="lines")
        st.plotly_chart(fig)
        if st.checkbox('Show details'):
            st.write(dict_)



URL = 'https://api.ohsome.org/v1/elements/count/density'

#lat = output['center']['lat']
#lon = output['center']['lng']
#rad = (output.get('last_circle_radius'))
#data = {"bcircles": f"{lon},{lat},{rad}", "format": "json", "time": "2022-05-07", "filter": "landuse=industrial"}
#st.write(data)
#response = requests.post(URL, data=data)
#st.write(response.json())

st.markdown(html, unsafe_allow_html=True)
