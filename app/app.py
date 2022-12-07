import streamlit as st
from PIL import Image

add_selector = st.sidebar.selectbox(
    "Pages",
    ("Home","Dashboards","Prediction")
)


image = Image.open('app/app_landing.png')
st.image(image)
