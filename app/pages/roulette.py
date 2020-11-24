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


@st.cache
def select_data(app):
    # Select tinder universe
    tinder_data = app.recipes[app.recipes['rating_count'] > 3].sort_values(by='rating_mean', ascending=False)

    # Filter tinder universe based on user preferences
    user_data = filters.all_filters(tinder_data, goal = app.user_prefs['goal'].values[0],
                                                 diet = app.user_prefs['diet'].values[0],
                                                 allergies = app.user_prefs['allergies'].values[0].split(", "),
                                                 dislikes = app.user_prefs['dislikes'].values[0].split(", "),
                                                 custom_dsl = app.user_prefs['custom_dsl'].values[0])

    print(f"User #{app.user_prefs['app_user_id'].values[0]} - {app.user_prefs['name'].values[0]}: {len(tinder_data)} > {len(user_data)}")

    return user_data


def get_recipe(app, data):
    rated_recipes_ids = app.user_rates.recipe_id.values
    roulette_data = data[~(data['recipe_id'].isin(rated_recipes_ids))]
    return roulette_data


def run(app):
    # Load info
    user_data = select_data(app)
    roulette_data = get_recipe(app, user_data)
    recipe = roulette_data.iloc[0]

    # Display headers
    st.write("# Food Roulette")
    st.write(f"♥️ Tell us what you like, {app.user_name.split(' ')[0]}!")
    st.markdown("---")

    draw_recipe(app, recipe, 'roulette')

