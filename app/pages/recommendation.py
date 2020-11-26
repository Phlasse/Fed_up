import pandas as pd
import pandas
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
from helpers import side_filters, clean_prefs


@st.cache(show_spinner=False)
def generate_recs(user_rates, user_prefs, recipes, cm, rm):
    user_inputs = {row['recipe_id']: row['liked'] for index, row in user_rates.iterrows()}

    if str(user_prefs.collab.values[0]) != 'nan':
        collab = float(user_prefs.collab)
    else:
        collab = 0.5

    recs = get_user_recommendations(user_inputs = user_inputs, collaborative = collab,
                                    content_latent = cm, rating_latent = rm)

    rec_recipes = recs.merge(recipes, on="recipe_id", how="left")

    goal, diet, allergies, dislikes, custom_dsl = clean_prefs(user_prefs)
    filtered_recs = filters.all_filters(rec_recipes, goal = goal,
                                                     diet = diet,
                                                     allergies = allergies,
                                                     dislikes = dislikes,
                                                     custom_dsl = custom_dsl)
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

    if len(app.user_rates) < 1:
        st.markdown("###### *No information about your tastes yet, please use our food roulette!*")

    else:
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
