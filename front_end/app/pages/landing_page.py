import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pydeck as pdk
from urllib.request import urlopen
import json


st.set_page_config(layout="wide")

# TITLE
st.markdown("""
    # Which is the best place to set up a Solar Panel Station?
    """)

# DB
spain_provinces = pd.read_csv("../../raw_data/provincias.csv")
solar_stations = pd.read_csv("../../raw_data/Spain_energy_df_2017.csv")
map_solar_stations = solar_stations[solar_stations["primary_fuel"]=="Solar"]

# INVESTMENT NEEDED
cost = 0
col1, col2, col3 = st.columns(3)
with col1:
    st.header("Solar energy production")
    option = st.slider('Compared to aggregated energy production (in %)', 5, 100, 5)
with col2:
    st.metric("Investment Needed", f"€{cost}")
    st.metric("Solar Stations", map_solar_stations.shape[0], option)
with col3:
    st.metric("Solar Energy produced (GWh)", "1234.5", option)
    st.metric("Non-renewable energy produced (GWh)", "67890.5", option)



# MAP WITH BORDERS
with urlopen('https://raw.githubusercontent.com/deldersveld/topojson/master/countries/spain/spain-province.json')\
    as response:
    Spain = json.load(response)
# MAP


# PLOTLY FIG
c1,c2 = st.columns(2)
fig = px.scatter_geo(map_solar_stations,lat='lat',lon='lon',
                     color="Solar Generation (2017)",
                     template="simple_white",
                     color_continuous_scale=px.colors.sequential.Greens,
                     title="Solar Stations in Spain by energy production (2017)"
                     )
fig.update_geos(
    center=dict(lon=-3.7038, lat=40.4168),
    lataxis_range=[1,7], lonaxis_range=[35, 45],
    visible=False, resolution=50, scope="europe",
    showcountries=True, countrycolor="Black",
    showsubunits=True, subunitcolor="White",
    showframe=False, showland=True,
)
fig.update_traces(marker=dict(size=12,
                              line=dict(width=1,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
fig.update(layout_coloraxis_showscale=False)
fig.update_layout(
    margin=dict(l=1, r=1, t=1, b=1),
    title_y=0.95
)
# PLOTLY FIG2
c1,c2 = st.columns(2)
fig2 = px.scatter_geo(map_solar_stations,lat='lat',lon='lon',
                     color="Solar Generation (2017)",
                     template="simple_white",
                     color_continuous_scale=px.colors.sequential.Blues,
                     title="Top 20 places to locate a new station",
                     #locations=spain_provinces["Provincia"],
                     #geojson=Spain
                     )
fig2.update_geos(
    center=dict(lon=-3.7038, lat=40.4168),
    lataxis_range=[1,7], lonaxis_range=[35, 45],
    visible=False, resolution=50, scope="europe",
    showcountries=True, countrycolor="Black",
    showsubunits=True, subunitcolor="White",
    showframe=False, showland=True,
)
fig2.update_traces(marker=dict(size=12,
                              line=dict(width=1,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
fig2.update(layout_coloraxis_showscale=False)
fig2.update_layout(
    margin=dict(l=1, r=1, t=1, b=1),
    title_y=0.95
)

c1.plotly_chart(fig, use_container_width =True)
c2.plotly_chart(fig2, use_container_width =True)
