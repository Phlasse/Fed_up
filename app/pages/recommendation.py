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

from Fed_up.pipeline import get_user_recommendations
from Fed_up import filters
from cards import draw_recipe
from helpers import side_filters


def generate_recs(app):
    user_inputs = {row['recipe_id']: row['liked'] for index, row in app.user_rates.iterrows()}

    recs = get_user_recommendations(user_inputs = user_inputs, collaborative = float(app.user_prefs.collab),
                                    content_latent = app.content_matrix, rating_latent = app.rating_matrix)

    rec_recipes = recs.merge(app.recipes, on="recipe_id", how="left")

    user_info = app.user_prefs
    filtered_recs = filters.all_filters(rec_recipes, goal = user_info['goal'].values[0],
                                                     diet = user_info['diet'].values[0],
                                                     allergies = user_info['allergies'].values[0].split(", "),
                                                     dislikes = user_info['dislikes'].values[0].split(", "),
                                                     custom_dsl = user_info['custom_dsl'].values[0])

    return filtered_recs


def run(app):
    # Display headers
    st.write("# Recommendations")
    st.write(f"🥘 Check the best dishes we have selected for you.")
    st.markdown("---")

    st.sidebar.markdown("---")
    st.sidebar.markdown("#### Feel free to adjust your search:")
    st.sidebar.markdown("    ")

    time, steps, ingreds, n_recipes = side_filters(app)

    data = generate_recs(app)
    disliked_recipe_ids = app.user_dislikes.recipe_id.values
    filtered_data = data[(~data.recipe_id.isin(disliked_recipe_ids)) & (data.minutes<=time) & (data.n_steps<=steps) & (data.n_ingredients<=ingreds)]

    if len(filtered_data.head(n_recipes)) > 0:
        for index, recipe in filtered_data.head(n_recipes).iterrows():
            draw_recipe(app, recipe, 'recommendation')
            st.markdown("---")

    else:
        st.markdown("###### *No additional recommendations to show, try adjusting your filters!*")
