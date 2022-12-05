import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
from urllib.request import urlopen
import difflib
import streamlit as st


# UPLOAD DATAFRAME
df = pd.read_csv("raw_data/Energy_Provinces.csv")
df = df.rename(columns={'energy_gen_gwh':'solar_generation'})
df.drop(['Unnamed: 0', 'country'], axis=1, inplace=True)
df = df.loc[df.primary_fuel=='Solar']

# LOAD JSON WITH PROVINCIAS AND THEIR LAT-LON POSITION
Spain = json.load(open('raw_data/spain.geojson', encoding='utf-8'))
# Create state id map
state_id_map = {}
for feature in Spain['features']:
    feature['id'] = feature['properties']['provincia']
    state_id_map[feature['properties']['cod_ccaa']] = feature['id']

print(state_id_map)


# FUNCTION TO LINK PROVINCE NAMES (ACCENTS AND SPECIAL CHARACTERS TO THE MOST
# SIMILAR ONES)
words = list(state_id_map.values())
def get_close_matches(word, words):
    split = word.split('/')
    if len(split)>1:
        word=split[0]
  # Then we find the closest match
    if len(difflib.get_close_matches(word, words, n=1)) > 0:
        return difflib.get_close_matches(word, words, n=1)[0]
    return word

# OVERWRITE PROVINCES WITH THE RIGHT NAMES
#df['province'] = df.province.apply(lambda x: get_close_matches(x, words))

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

st.dataframe(df)

# SHOW MAP
fig = px.choropleth(
 data,
 locations = 'province', #define the limits on the map/geography
 locationmode='geojson-id',
 geojson = Spain, #shape information
 color = "solar_generation", #defining the color of the scale through the database
 hover_name = 'province', #the information in the box
 color_continuous_scale="Viridis",
 range_color=(data.solar_generation.min(), data.solar_generation.max()),
 )

#fig.update_geos(
#    lonaxis_range= [no_cruz_palmas.lon.min()-3,no_cruz_palmas.lon.max()+3], lataxis_range= [no_cruz_palmas.lat.min(), no_cruz_palmas.lat.max()+1]
#)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Add number of customers as orange markers
fig.add_trace(
    go.Scattergeo(
                lon = data["lon"],
                lat = data["lat"],
                textposition="middle right",
                text = data['primary_fuel'],
                mode = 'markers',
                marker = dict(size = data['primary_fuel'], color = 'orange', opacity=0.9))
    )
fig.update_geos(
    center=dict(lon=-3.7038, lat=40.4168),
    lataxis_range=[1,7], lonaxis_range=[35, 45],
    visible=False, resolution=50, scope="europe",
    showcountries=True, countrycolor="Black",
    showsubunits=True, subunitcolor="White",
    showframe=False, showland=True,
)

st.plotly_chart(fig, use_container_width=True)
