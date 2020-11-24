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


def save_like(app, rid, liked):
    info = app.user_likes[app.user_likes.recipe_id == rid]

    if len(info) == 1:
        index = info.index[0]
        app.likes.loc[index, 'liked'] = liked
        app.likes.loc[index, 'timestamp'] = pd.Timestamp.now()
    else:
        app.likes = app.likes.append({'app_user_id': app.user_id, 'recipe_id': rid, 'liked': liked, 'timestamp': pd.Timestamp.now()}, ignore_index=True)

    app.likes.to_csv(app.likes_path, index=False)


def clear_like(app, rid):
    info = app.user_likes[app.user_likes.recipe_id == rid]

    if len(info) == 1:
        index = info.index[0]
        app.likes.drop(app.likes.index[index], inplace=True)
        app.likes.to_csv(app.likes_path, index=False)


def add_to_checkout(app, rid):
    info = app.checkouts[app.checkouts.recipe_id == rid]

    if len(info) < 1:
        app.checkouts = app.checkouts.append({'app_user_id': app.user_id, 'recipe_id': rid, 'timestamp': pd.Timestamp.now()}, ignore_index=True)
        app.checkouts.to_csv(app.checkouts_path, index=False)


def remove_from_checkout(app, rid):
    info = app.checkouts[app.checkouts.recipe_id == rid]

    if len(info) == 1:
        index = info.index[0]
        app.checkouts.drop(app.checkouts.index[index], inplace=True)
        app.checkouts.to_csv(app.checkouts_path, index=False)


def draw_recipe(app, recipe, scope):
    recipe_show, _space, recipe_liker = st.beta_columns([4, 0.5, 1])

    with recipe_show: # Display next item
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
                save_like(app, recipe.recipe_id, 1)
                st.experimental_rerun()

            if st.button('👎 Dislike'):
                save_like(app, recipe.recipe_id, 0)
                st.experimental_rerun()

            st.markdown("---")

            st.write(f"###### {len(app.user_likes)} Liked")
            st.write(f"###### {len(app.user_dislikes)} Disliked")

        elif scope == 'recommendation' or scope == 'liked':

            st.write(" ")

            if recipe.recipe_id in list(app.user_checkouts.recipe_id.values):
                value = True
            else:
                value = False

            ckout = st.checkbox("Checkout", value=value, key=f'ckout-{recipe.recipe_id}')

            if ckout:
                add_to_checkout(app, recipe.recipe_id)
            else:
                remove_from_checkout(app, recipe.recipe_id)

            liked_recipes_ids = app.user_likes.recipe_id.values
            if recipe.recipe_id not in list(liked_recipes_ids):
                if st.button('👍 Like', f'like-{recipe.recipe_id}'):
                    save_like(app, recipe.recipe_id, 1)
                    st.experimental_rerun()
            else:
                if st.button('✋ Unlike', f'like-{recipe.recipe_id}'):
                    clear_like(app, recipe.recipe_id)
                    st.experimental_rerun()

            if st.button('👎 Dislike', f'dislike-{recipe.recipe_id}'):
                save_like(app, recipe.recipe_id, 0)
                st.experimental_rerun()

            st.markdown("---")

            st.write(f'###### Rating: {np.round(float(recipe.rating_mean), 2)}')
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
