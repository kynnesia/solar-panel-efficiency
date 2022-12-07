import streamlit as st
from PIL import Image

image = Image.open('app_landing.png')
st.image(image)
