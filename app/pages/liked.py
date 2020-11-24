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

from Fed_up import filters
from cards import draw_recipe


def run(app):

    st.write("# Liked Recipes")
    st.write(f"👍 Revisit your favorite recipes at any moment!")
    st.markdown("---")

    st.sidebar.markdown("---")
    st.sidebar.markdown("#### Feel free to adjust your search:")
    st.sidebar.markdown("    ")

    time = st.sidebar.slider("How long are you willing to wait?", 15, 120, 120)
    steps = st.sidebar.slider("How many steps are you willing to execute?", 3, 20, 20)
    n_ingreds = st.sidebar.slider("How many ingredients are you willing to use?", 3, 25, 25)

    liked_recipes = app.user_likes.sort_values(by='timestamp', ascending=False)
    data = liked_recipes.merge(app.recipes, on='recipe_id', how='inner')
    filtered_data = data[(data.minutes<=time) & (data.n_steps<=steps) & (data.n_ingredients<=n_ingreds)]

    for index, recipe in filtered_data.iterrows():
        draw_recipe(app, recipe, 'liked')
        st.markdown("---")
