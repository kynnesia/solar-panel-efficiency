import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from urllib.request import urlopen
import math
import pydeck as pdk
from pydeck.types import String
from unidecode import unidecode
import os


st.set_page_config(layout="wide")

#------- TITLE -------
st.markdown("""
    # Which is the best place to set up a Solar Panel Station?
    """)

#------- NOTES -------
pricexpanel = 125
gwhxpanel = 550 / 1_000_000
panelsxstation = 200_000
investmentxstation = pricexpanel*panelsxstation/1_000_000
energyxstation = gwhxpanel*panelsxstation

#------- DB -------
provincias = pd.read_csv("../../raw_data/provincias.csv")
solar_stations = pd.read_csv("../../raw_data/Spain_energy_df_2017.csv")
map_solar_stations = solar_stations[solar_stations["primary_fuel"]=="Solar"]
solar_energy = map_solar_stations["energy_gen_gwh"].sum()
all_energy = solar_stations["energy_gen_gwh"].sum()
actual_ratio_solar = (solar_energy/all_energy)*100
non_renewables_split = 0.677

#------- SLIDER AND DESCRIPTION -------
col1, col2 = st.columns(2)
with col1:
    st.header("Solar energy production")
    option = st.slider('Compared to aggregated energy production (in %)', 0, 100, math.ceil(actual_ratio_solar))
with col2:
    st.markdown("This is an ongoing project that aims to improve the decision-\
        making process concerning where to set up new Solar Stations. To do \
        so, we have analysed some features, mostly weather-related, to predict\
        those locations mostly suited to benefit from solar power.")
    if st.checkbox('Show metrics description'):
        st.write('''
            The number of incremental Solar Stations and Investment needed\
                are estimations based on real data. \
                Each Solar Station represents 200 thousand solar panels, and each\
                panel is estimated to cost around ~125€.
                We also assume that each incremental GWh generated by \
                solar energy will avoid 300 tones of CO2 per year.

            ''')

#------- METRICS -------
cost = 0
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Investment Needed (m€)", investmentxstation*round(option*(map_solar_stations.shape[0]/actual_ratio_solar)-246))
c2.metric("Solar Stations", round(option*(map_solar_stations.shape[0]/actual_ratio_solar)), -246+round(option*(map_solar_stations.shape[0]/actual_ratio_solar)))
c3.metric("Solar Energy produced (GWh)", int(all_energy)*option/100, round(int(all_energy)*option/100 - solar_energy, 2))
c4.metric("Decrease of CO2 (yearly/tons)", -round(int(all_energy)*option/100 - solar_energy, 2)*300)
c5.metric("Aggregate energy produced (GWh)", round(all_energy,2))


#------- PREPRO PROVINCIAS -------
provincias["Provincia"] = provincias["Provincia"].apply(unidecode)
#------- MAP PREPRO -------
provincias_grouped = provincias.groupby('Provincia').agg({'latitude':'mean','longitude':'mean'}).reset_index()
def get_closest_province(row):
    df = provincias_grouped[['latitude','longitude']] - list(row[['lat','lon']])

    df['agg'] = df['latitude']**2 + df['longitude']**2
    name_index = df.sort_values('agg').iloc[0,:].name

    return provincias_grouped.iloc[name_index].Provincia
map_solar_stations['province'] = map_solar_stations.apply(get_closest_province,axis=1)
map_solar_stations.groupby('province').agg({'energy_gen_gwh':'sum'}).sort_values('energy_gen_gwh',ascending=False)
#------- MAP  -------
data = map_solar_stations
layer = pdk.Layer(
    "GridLayer",
    data,
    pickable=True,
    extruded=True,
    stroked=False,
    filled=True,
    wireframe=True,
    cell_size=15000,
    elevation_scale=200,
    get_position=['lon', 'lat'],
)
layer2 = pdk.Layer(
    "HeatmapLayer",
    data,
    opacity=0.5,
    get_position=['lon', 'lat'],
    aggregation=String('SUM'),
    get_weight="energy_gen_gwh")
view_state = pdk.ViewState(latitude=43.5528	, longitude=-5.7231, zoom=5, bearing=0, pitch=45)

# Render
r = pdk.Deck(
    layers=[layer,layer2],
    initial_view_state=view_state,
    tooltip={"text": "{position}\nSolar Generation: {energy_gen_gwh}"},
)
st.pydeck_chart(r)


# PLOTLY FIG
c1,c2 = st.columns(2)
fig = px.scatter_geo(map_solar_stations,lat='lat',lon='lon',
                     color="energy_gen_gwh",
                     template="simple_white",
                     color_continuous_scale=px.colors.sequential.Greens)
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
                     color="energy_gen_gwh",
                     template="simple_white",
                     color_continuous_scale=px.colors.sequential.Blues)
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
with c1:
    st.header("Solar Stations in Spain | 2017")
    st.write("Description")
    st.plotly_chart(fig, use_container_width =True)
with c2:
    st.header("Most Efficienct locations")
    st.write("Description")
    st.plotly_chart(fig2, use_container_width =True)
