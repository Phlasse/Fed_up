import pandas as pd
import numpy as np

import streamlit as st
import streamlit.components.v1 as components

import base64
from PIL import Image
from io import BytesIO
import requests
import ipdb
import time
import os

from cards import draw_recipe


# @st.cache
def generate_recs(app, collab):
    return app.recipes


def run(app):
    # Display headers
    st.write("# Recommendations")
    st.write(f"🥘 Check the best dishes we have selected for you.")
    st.markdown("---")

    st.sidebar.markdown("---")
    st.sidebar.markdown("#### Feel free to adjust your search:")
    st.sidebar.markdown("    ")

    time = st.sidebar.slider("How long are you willing to wait?", 15, 120, 60)
    steps = st.sidebar.slider("How many steps are you willing to execute?", 3, 20, 7)
    n_ingreds = st.sidebar.slider("How many ingredients are you willing to use?", 3, 25, 13)
    n_recipes = st.sidebar.slider("How many recommendations do you want to see?", 5, 40, 5)
    collab = st.sidebar.slider("How much would you like to try new flavors?", 0, 100, 50)

    data = generate_recs(app, collab)
    filtered_data = data[(data.minutes<=time) & (data.n_steps<=steps) & (data.n_ingredients<=n_ingreds)]

    for index, recipe in filtered_data.head(n_recipes).iterrows():
        draw_recipe(app, recipe, 'recommendation')
        st.markdown("---")
