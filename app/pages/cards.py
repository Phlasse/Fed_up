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


def save_like(user_recipes, user_id, rid, liked):
    user_recipes = user_recipes.append({'app_user_id': user_id, 'recipe_id': rid, 'liked': liked}, ignore_index=True)
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_likes.csv")) # TO DO: DEFINE PROPER PATH
    user_recipes.to_csv(csv_path, index=False)


def draw_recipe(recipe, scope, user_id=None, user_recipes=None):
    recipe_show_1, space, recipe_liker = st.beta_columns([4, 0.2, 1])

    with recipe_show_1: # Display next item
        title = recipe['name'].replace(" s ", "'s ").upper()
        st.write(f"### **{title}**")
        st.write(" ")

        # description = (". ").join([sentence.capitalize() for sentence in recipe.description.split(". ")])
        # st.write(f"###### {description}")
        # st.write(" ")


    with recipe_liker: # Manage option

        if scope == 'roulette':

            st.write(" ")

            if st.button('👍 Like'):
                save_like(user_recipes, user_id, recipe.recipe_id, 1)
                st.experimental_rerun()

            if st.button('👎 Dislike'):
                save_like(user_recipes, user_id, recipe.recipe_id, 0)
                st.experimental_rerun()

            st.markdown("---")

            st.write(f"###### {len(user_recipes[(user_recipes['liked'] == 1) & (user_recipes['app_user_id'] == user_id)])} Liked")
            st.write(f"###### {len(user_recipes[(user_recipes['liked'] == 0) & (user_recipes['app_user_id'] == user_id)])} Disliked")

        elif scope == 'recommendation':

            st.write(" ")

            # st.button('Temp')

            st.markdown("---")

            st.write(f'###### Rating: {float(recipe.rating_mean)}')
            st.write(f'###### Reviews: {int(recipe.rating_count)}')

            st.markdown("---")

            st.write(f'###### **Calories: {float(recipe.calories)} Cal**')
            st.write(f'###### Total fat: {float(recipe.total_fat)} %')
            st.write(f'###### Saturated fat: {float(recipe.saturated_fat)} %')
            st.write(f'###### Sugar: {float(recipe.sugar)} %')
            st.write(f'###### Sodium: {float(recipe.sodium)} %')
            st.write(f'###### Protein: {float(recipe.protein)} %')
            st.write(f'###### Carbs: {float(recipe.carbohydrates)} %')
            st.write(' ')
            st.write(f'###### *For a daily intake of 2000 calories*')

    st.write(" ")
