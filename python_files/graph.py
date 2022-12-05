import streamlit as st
import pandas as pd
import numpy as np
from data_graph_streamlit import get_lat_lon

st.map(get_lat_lon())