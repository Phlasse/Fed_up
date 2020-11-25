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
from helpers import side_filters


def run(app):
    # Display headers
    st.write("# Liked Recipes")
    st.write(f"👍 Revisit your favorite recipes at any moment!")
    st.markdown("---")

    st.sidebar.markdown("---")
    st.sidebar.markdown("#### Feel free to adjust your search:")
    st.sidebar.markdown("    ")

    time, steps, ingreds, n_recipes = side_filters(app)

    liked_recipes = app.user_likes.sort_values(by='timestamp', ascending=False)
    data = liked_recipes.merge(app.recipes, on='recipe_id', how='inner')
    filtered_data = data[(data.minutes<=time) & (data.n_steps<=steps) & (data.n_ingredients<=ingreds)]

    if len(filtered_data.head(n_recipes)) > 0:
        for index, recipe in filtered_data.head(n_recipes).iterrows():
            draw_recipe(app, recipe, 'liked')
            st.markdown("---")

    elif len(app.user_likes) == 0:
        st.markdown("###### *No liked recipes, try our food roulette!*")

    else:
        st.markdown("###### *No recipes to show, try adjusting your filters!*")
