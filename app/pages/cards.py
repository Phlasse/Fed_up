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

import storage


def draw_recipe(app, recipe, scope):
    recipe_show, _space, recipe_liker = st.beta_columns([4, 0.5, 1])

    with recipe_show: # Display next item
        title = recipe['name'].replace(" s ", "'s ").upper()
        st.write(f"### **{title}**")
        st.write(" ")

        response_pic = requests.get(recipe['image_url'])
        img = Image.open(BytesIO(response_pic.content))
        st.image(img, width=500)

        if scope == 'recommendation':
            st.progress(int(recipe['rec_score']*100))

        st.write(" ")


        # description = (". ").join([sentence.strip().capitalize() for sentence in recipe.description.split("."|"!")])
        # st.write(f"{description}")

        clean_ingredients = [ing.strip().lower() for ing in eval(recipe['ingredients'])]
        ingredients = (", ").join(clean_ingredients)
        st.write(f"**Ingredients ({len(clean_ingredients)}):** {ingredients}.")

        clean_steps = [step.strip().lower() for step in eval(recipe['steps'])]
        steps = (", ").join(clean_steps)
        st.write(f"**Steps ({len(clean_steps)}):** {steps}.")


    with recipe_liker: # Manage option

        if scope == 'roulette':

            st.write(" ")

            if st.button('👍 Like'):
                storage.save_like(app, recipe.recipe_id, 1)
                st.experimental_rerun()

            if st.button('👎 Dislike'):
                storage.save_like(app, recipe.recipe_id, 0)
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
                storage.add_to_checkout(app, recipe.recipe_id)
                # st.experimental_rerun()
            else:
                storage.remove_from_checkout(app, recipe.recipe_id)
                # st.experimental_rerun()

            liked_recipes_ids = app.user_likes.recipe_id.values
            if recipe.recipe_id not in list(liked_recipes_ids):
                if st.button('👍 Like', f'like-{recipe.recipe_id}'):
                    storage.save_like(app, recipe.recipe_id, 1)
                    st.experimental_rerun()
            else:
                if st.button('✋ Unlike', f'like-{recipe.recipe_id}'):
                    storage.clear_like(app, recipe.recipe_id)
                    # storage.remove_from_checkout(app, recipe.recipe_id)
                    st.experimental_rerun()

            if st.button('👎 Dislike', f'dislike-{recipe.recipe_id}'):
                storage.save_like(app, recipe.recipe_id, 0)
                # storage.remove_from_checkout(app, recipe.recipe_id)
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
