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


@st.cache
def load_result():
    user_id = 2 # TO DO: GET USER ID
    recipe_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "Fed_up/data/samples/recipe_sample.csv")) # TO DO: DEFINE PROPER PATH
    prefs_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_prefs.csv")) # TO DO: DEFINE PROPER PATH

    data = pd.read_csv(recipe_csv_path)
    tinder_data = data[data['rating_count'] > 3].sort_values(by='rating_mean', ascending=False)

    user_prefs = pd.read_csv(prefs_csv_path)
    user = user_prefs[user_prefs.app_user_id == user_id]

    user_data = filters.all_filters(tinder_data, goal = user['goal'].values[0],
                                                 diet = user['diet'].values[0],
                                                 allergies = user['allergies'].values[0].split(", "),
                                                 dislikes = user['dislikes'].values[0].split(", "),
                                                 custom_dsl = user['custom_dsl'].values[0])

    print(f"User #{user['app_user_id'].values[0]} - {user['name'].values[0]}: {len(tinder_data)} > {len(user_data)}")

    return user_data, user


def get_recipe(data, user):
    # Get user info
    user_id = user['app_user_id'].values[0]
    user_fname = user['name'].values[0].split(" ")[0]

    # Select next item
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_likes.csv")) # TO DO: DEFINE PROPER PATH
    user_recipes = pd.read_csv(csv_path)
    rated_recipes = user_recipes[user_recipes.app_user_id == user_id].recipe_id.values
    roulette_data = data[~(data['recipe_id'].isin(rated_recipes))]

    return user_id, user_fname, user_recipes, roulette_data


def save_like(user_recipes, user_id, rid, liked):
    user_recipes = user_recipes.append({'app_user_id': user_id, 'recipe_id': rid, 'liked': liked}, ignore_index=True)
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_likes.csv")) # TO DO: DEFINE PROPER PATH
    user_recipes.to_csv(csv_path, index=False)


def run():
    # Load info
    data, user = load_result()
    user_id, user_fname, user_recipes, roulette_data = get_recipe(data, user)
    title = roulette_data.iloc[0]['name'].replace(" s ", "'s ").upper()
    rid = roulette_data.iloc[0]['recipe_id']

    # Display headers
    st.write("# Food Roulette")
    st.write(f"♥️ Tell us what you like, {user_fname}!")
    st.markdown("---")

    recipe_show, recipe_liker = st.beta_columns([5, 1])

    with recipe_show: # Display next item
        st.write(f"### **{title}**")
        st.write(" ")

    with recipe_liker: # Manage option
        st.write(" ")

        if st.button('👍 Like'):
            save_like(user_recipes, user_id, rid, 1)
            st.experimental_rerun()

        if st.button('👎 Dislike'):
            save_like(user_recipes, user_id, rid, 0)
            st.experimental_rerun()

        st.markdown("---")

        st.write(f"###### {len(user_recipes[(user_recipes['liked'] == 1) & (user_recipes['app_user_id'] == user_id)])} Liked")
        st.write(f"###### {len(user_recipes[(user_recipes['liked'] == 0) & (user_recipes['app_user_id'] == user_id)])} Disliked")


