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
import plotly.graph_objects as go
import json
from geopy.geocoders import Nominatim


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
provincias = pd.read_csv("app/pages/raw_data/provincias.csv")
solar_stations = pd.read_csv("app/pages/raw_data/Spain_energy_df_2017.csv")
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
view_state = pdk.ViewState(latitude=40.396765, longitude=-3.71338, zoom=5, bearing=0, pitch=45)

# Render
r = pdk.Deck(
    layers=[layer,layer2],
    initial_view_state=view_state,
    tooltip={"text": "{position}\nSolar Generation: {energy_gen_gwh}"},
)

st.pydeck_chart(r)


# UPLOAD DATAFRAME
df = pd.read_csv("app/pages/raw_data/Energy_Provinces.csv")
df = df.rename(columns={'energy_gen_gwh':'solar_generation'})
df.drop(['Unnamed: 0', 'country'], axis=1, inplace=True)
df = df.loc[df.primary_fuel=='Solar']
# LOAD JSON WITH PROVINCIAS AND THEIR LAT-LON POSITION
Spain = json.load(open('app/pages/raw_data/spain.geojson', encoding='utf-8'))
# Create state id map
state_id_map = {}
for feature in Spain['features']:
    feature['id'] = feature['properties']['provincia']
    state_id_map[feature['properties']['cod_ccaa']] = feature['id']
# CREATE A LAT-LON DICT TO CREATE ROWS FOR PROVINCIAS THAT ARE NOT IN THE DF
lat_lon = {}
for each in Spain['features']:
  lat_lon[each['properties']['provincia']] = each['properties']['geo_point_2d']
for each in list(state_id_map.values()):
  if each not in df.province:
    new_row = { 'lat':lat_lon[each][0],
            'lon':lat_lon[each][1],
#So that we dont have empty spaces - we fill in states with no solar with 0
            'solar_generation':0,
            'capacity_mw':0,
            'primary_fuel':'Solar',
            'province':each}
    df = df.append(new_row, ignore_index=True)
# GROUP BY
data = df.groupby('province').agg({'solar_generation':'sum',
                                               'primary_fuel':'count',
                                               'lat':'mean',
                                               'lon':'mean'}).reset_index()
# FIGURE 1
fig1 = px.choropleth(
 data,
 locations = 'province', #define the limits on the map/geography
 locationmode='geojson-id',
 geojson = Spain, #shape information
 color = "solar_generation", #defining the color of the scale through the database
 hover_name = 'province', #the information in the box
 color_continuous_scale="Greens",
 range_color=(data.solar_generation.min(), data.solar_generation.max()),
 )
fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig1.add_trace(
#    go.Scattergeo(
#                lon = data["lon"],
#                lat = data["lat"],
#                textposition="middle right",
#                text = data['primary_fuel'],
#                mode = 'markers',
#                marker = dict(size = data['primary_fuel'], color = 'orange', opacity=0.9))
#    )
fig1.update_geos(
    center=dict(lon=-3.7038, lat=40.4168),
    lataxis_range=[1,7], lonaxis_range=[35, 45],
    visible=False, resolution=50, scope="europe",
    showcountries=True, countrycolor="Black",
    showsubunits=True, subunitcolor="White",
    showframe=False, showland=True,
)

# FIGURE 2
fig2 = px.choropleth(
 data,
 locations = 'province', #define the limits on the map/geography
 locationmode='geojson-id',
 geojson = Spain, #shape information
 color = "primary_fuel", #defining the color of the scale through the database
 hover_name = 'province', #the information in the box
 color_continuous_scale="Oranges",
 range_color=(data.primary_fuel.min(), data.primary_fuel.max()),
 )
fig2.update_geos(
    center=dict(lon=-3.7038, lat=40.4168),
    lataxis_range=[1,7], lonaxis_range=[35, 45],
    visible=False, resolution=50, scope="europe",
    showcountries=True, countrycolor="Black",
    showsubunits=True, subunitcolor="White",
    showframe=False, showland=True,
)
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


col1,col2=st.columns(2)

with col1:
    st.header("Solar Stations per region in Spain | 2017")
    if st.checkbox('Solar Stations Graph Description'):
        st.write(f"As of 2017, Spain had {map_solar_stations.shape[0]} Solar\
        Stations. Here, they are classified by their energy production.")
    st.plotly_chart(fig2, use_container_width =True)
with col2:
    st.header("Energy generated per region in Spain | 2017")
    if st.checkbox('Locations Graph Description'):
        st.write("By training a supervised model that considered all Solar\
        Stations around the globe, learns which features influence the\
        generation of solar energy, and recommends the most suitable\
        spots to install new stations.")
    st.plotly_chart(fig1, use_container_width =True)


#------- PREDICTION MAP  -------
pred_df = pd.read_csv('app/pages/raw_data/Predictions_with_City_Spain.csv')
pred_df["production prediction"] = np.exp(pred_df["production prediction"])
lat_lon_pred = pred_df[["latitude","longitude","production prediction"]]

layer = pdk.Layer(
    "GridLayer",
    lat_lon_pred,
    pickable=True,
    extruded=True,
    stroked=False,
    filled=True,
    wireframe=True,
    colorRange=[[255,255,204],[217,240,163],[173,221,142],
                [120,198,121],[49,163,84], [0,104,55]],
    cell_size=10000,
    elevation_scale=200,
    get_position=['longitude', 'latitude'],
)
view_state = pdk.ViewState(latitude=40.396765, longitude=-3.71338, zoom=5, bearing=0, pitch=45)

# Render
pred_graph = pdk.Deck(
    layer,
    initial_view_state=view_state,
    tooltip={"text": "{position}\nPredicted Solar Generation: {energy_gen_gwh}"},
)

st.header("Estimated solar energy generated by +8.000 Spain locations")
st.write("Description of the graph")
st.pydeck_chart(pred_graph)

geolocator = Nominatim(user_agent="geoapiExercises")
st.dataframe(pred_df[["City","production prediction"]].sort_values(by="production prediction", ascending=False))
