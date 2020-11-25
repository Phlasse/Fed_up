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

def run(app):
    # Display headers
    checkout_ids = app.user_checkouts
    selected_recipe_ids=[236834]#, 265381, 283173]
    recipe_df = app.recipes
    selected_recipes_df = recipe_df[recipe_df.recipe_id.isin(selected_recipe_ids)]
    st.write("# Checkout")
    st.write(f"🛒 Confirm and export your selected dishes.")
    st.markdown("---")
    summed_ingredients = {}

    st.header("Session's recipes for checkout:")
    #selection_ingredients =
    #st.write(selected_recipes_df)
    for i in range(len(selected_recipes_df["recipe_id"])):
        st.write("*", list(selected_recipes_df.name)[i].capitalize())
        temp_ingredients = list(selected_recipes_df.ingredients)[i]#.split("',")
        for j in temp_ingredients.split("',"):
            ji = j.replace("[", "").replace("]", "").replace("'", "")
            if ji in summed_ingredients:
                summed_ingredients[ji] += 1#*persons
            else:
                summed_ingredients[ji] = 1#*persons
    st.header("Here is your grocery list:")
    ing_list_exp = pd.DataFrame()
    ing_list_exp["Ingredient"] = list(summed_ingredients.keys())
    ing_list_exp["Quantity"] = list(summed_ingredients.values())
    #################################
    ### Export to Microsoft To Do ###
    #################################
    #ToDo = st.button("Export to Microsoft to do")
    #if ToDo:

    #    for key, value in summed_ingredients.items():
    #        call_url= f"https://hook.integromat.com/5oboi86rrbc1qsf5koeulfmtwn76c9qg?Subject={key}%20{value}%20x&note=Subscribe%20to%20Fed-up&list=Fed-up"
    #        call = requests.get(call_url)

    ###########################
    ### weird export option ###
    ###########################
    txt = ing_list_exp.to_csv(index = False)
    b64 = base64.b64encode(txt.encode()).decode()
    href = f'<a href="data:file/ingredients.txt;base64,{b64}">Download</a> (right-click and save as Grocery.txt)'
    st.markdown(href, unsafe_allow_html=True)
    st.table(ing_list_exp)

