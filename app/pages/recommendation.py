import pandas as pd
import numpy as np

import streamlit as st
import streamlit.components.v1 as components

import base64
from PIL import Image
from io import BytesIO
import requests
import time
import os

from Fed_up.pipeline import get_user_recommendations
from Fed_up import filters
from cards import draw_recipe
from helpers import side_filters


@st.cache(show_spinner=False)
def generate_recs(user_rates, user_prefs, recipes, cm, rm):
    user_inputs = {row['recipe_id']: row['liked'] for index, row in user_rates.iterrows()}

    recs = get_user_recommendations(user_inputs = user_inputs, collaborative = float(user_prefs.collab),
                                    content_latent = cm, rating_latent = rm)

    rec_recipes = recs.merge(recipes, on="recipe_id", how="left")

    filtered_recs = filters.all_filters(rec_recipes, goal = user_prefs['goal'].values[0],
                                                     diet = user_prefs['diet'].values[0],
                                                     allergies = user_prefs['allergies'].values[0].split(", "),
                                                     dislikes = user_prefs['dislikes'].values[0].split(", "),
                                                     custom_dsl = user_prefs['custom_dsl'].values[0])
    return filtered_recs


def run(app):
    # Display headers
    st.write("# Recommendations")
    st.write(f"🥘 Check the best dishes we have selected for you.")
    st.markdown("---")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Filters")
    st.sidebar.markdown("    ")

    search, time, steps, ingreds, n_recipes = side_filters(app)

    data = generate_recs(app.user_rates, app.user_prefs, app.recipes, app.content_matrix, app.rating_matrix)

    filtered_data = data[(data.minutes<=time) & (data.n_steps<=steps) & (data.n_ingredients<=ingreds)]
    filtered_data = filtered_data.drop_duplicates()

    if search:
        filtered_data = filtered_data[filtered_data.metadata.str.contains(search)]

    if len(filtered_data.head(n_recipes)) > 0:
        for index, recipe in filtered_data.head(n_recipes).iterrows():
            draw_recipe(app, recipe, 'recommendation')
            st.markdown("---")

    else:
        st.markdown("###### *No additional recommendations to show, try adjusting your filters!*")
