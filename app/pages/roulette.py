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

from Fed_up import filters
from cards import draw_recipe


@st.cache(show_spinner=False)
def select_data(recipes, prefs):
    # Select tinder universe
    tinder_data = recipes[recipes['rating_count'] > 3].sort_values(by='rating_mean', ascending=False)

    # Filter tinder universe based on user preferences
    user_data = filters.all_filters(tinder_data, goal = prefs['goal'].values[0],
                                                 diet = prefs['diet'].values[0],
                                                 allergies = prefs['allergies'].values[0].split(", "),
                                                 dislikes = prefs['dislikes'].values[0].split(", "),
                                                 custom_dsl = prefs['custom_dsl'].values[0])

    # print(f"User #{prefs['app_user_id'].values[0]} - {prefs['name'].values[0]}: {len(tinder_data)} > {len(user_data)}")

    if len(user_data) == 0:
        return None
    return user_data


def get_recipe(app, data):
    rated_recipes_ids = app.user_rates.recipe_id.values
    roulette_data = data[~(data['recipe_id'].isin(rated_recipes_ids))]
    return roulette_data


def run(app):
    # Display headers
    st.write("# Food Roulette")
    st.write(f"♥️ Tell us what you like, {app.user_name.split(' ')[0]}!")
    st.markdown("---")

    # Load info
    user_data = select_data(app.recipes, app.user_prefs)

    if user_data is None:
        st.markdown("###### *No recipes left, try adjusting your preferences!*")

    else:
        roulette_data = get_recipe(app, user_data)
        recipe = roulette_data.iloc[0]
        draw_recipe(app, recipe, 'roulette')


