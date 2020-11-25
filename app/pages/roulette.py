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

@st.cache(suppress_st_warning=True)
def select_data(app):
    # Select tinder universe
    tinder_data = app.recipes[app.recipes['rating_count'] > 3].sort_values(by='rating_mean', ascending=False)

    # Filter tinder universe based on user preferences
    user_info = app.user_prefs
    user_data = filters.all_filters(tinder_data, goal = user_info['goal'].values[0],
                                                 diet = user_info['diet'].values[0],
                                                 allergies = user_info['allergies'].values[0].split(", "),
                                                 dislikes = user_info['dislikes'].values[0].split(", "),
                                                 custom_dsl = user_info['custom_dsl'].values[0])

    print(f"User #{user_info['app_user_id'].values[0]} - {user_info['name'].values[0]}: {len(tinder_data)} > {len(user_data)}")

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
    user_data = select_data(app)

    if user_data is None:
        st.markdown("###### *No recipes left, try adjusting your preferences!*")

    else:
        roulette_data = get_recipe(app, user_data)
        recipe = roulette_data.iloc[0]
        draw_recipe(app, recipe, 'roulette')


