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


@st.cache
def load_result():
    user_id = 2 # TO DO: GET USER ID
    recipe_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "Fed_up/data/samples/recipe_sample.csv")) # TO DO: DEFINE PROPER PATH
    prefs_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_prefs.csv")) # TO DO: DEFINE PROPER PATH

    data = pd.read_csv(recipe_csv_path)
    return data, user_id


def run():
    # Display headers
    st.write("# Recommendations")
    st.write(f"🍲 Check the best dishes we have selected for you.")
    st.markdown("---")

    st.sidebar.markdown("---")
    st.sidebar.markdown("#### Feel free to adjust your search:")
    st.sidebar.markdown("    ")

    time = st.sidebar.slider("How long are you willing to wait?", 15, 120, 60)
    steps = st.sidebar.slider("How many steps are you willing to execute?", 3, 20, 7)
    n_ingreds = st.sidebar.slider("How many ingredients are you willing to use?", 3, 25, 13)
    flavors = st.sidebar.slider("How much would you like to try new flavors?", 0, 100, 50)
    n_recipes = st.sidebar.slider("How many recipes do you want to show?", 5, 40, 5)

    data, user_id = load_result()
    filtered_data = data[(data.minutes<=time) & (data.n_steps<=steps) & (data.n_ingredients<=n_ingreds)]

    for index, recipe in filtered_data.head(n_recipes).iterrows():
        draw_recipe(recipe, 'recommendation', user_id)
        st.markdown("---")
