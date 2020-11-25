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


LIST_DIET = ['Classic', 'Pescetarian', 'Vegetarian', 'Vegan']

LIST_GOAL = ['Maintain Weight','Lose Weight','Gain Weight','Build Muscle']

ALLERGIES = ['Milk','Eggs','Fish','Shellfish','Tree Nuts','Peanuts','Wheat','Soybeans','Mustard']

DISLIKES = {
    'Beets': ['beet'],
    'Bell Peppers': ['bell pepper'],
    'Blue Cheese': ['blue cheese'],
    'Brussels Sprouts': ['brussels sprout'],
    'Cauliflower': ['cauliflower'],
    'Eggs': ['eggs'],
    'Goat Cheese': ['goat cheese'],
    'Mushrooms': ['mushroom'],
    'Olives':['olive'],
    'Quinoa':['quinoa'],
    'Shrimp':['shrimp'],
    'Tofu':['tofu'],
    'Turnips':['turnip']
}


def run(app):
    # Display headers
    st.write("# Profile")
    st.write(f"🙎 Please update your personal preferences.")
    st.markdown("---")

    user_info = app.user_prefs

    if str(user_info.name.values[0]) == 'nan':
        name_default = ''
    else:
        name_default = user_info.name.values[0]

    name = st.text_input("What is your name?", value=name_default)
    st.write(' ')

    if str(user_info.diet.values[0]) == 'nan':
        diet_selected = 0
    else:
        diet_selected = LIST_DIET.index(user_info.diet.values[0].title())

    diet = st.selectbox("Pick your diet:", tuple(diet for diet in LIST_DIET), diet_selected)
    st.write(' ')

    if str(user_info.goal.values[0]) == 'nan':
        goal_selected = 0
    else:
        goal_selected = LIST_GOAL.index(user_info.goal.values[0].title())

    goal = st.selectbox("Pick your nutritional goal:", tuple(goal for goal in LIST_GOAL), goal_selected)
    st.write(' ')

    if str(user_info.allergies.values[0]) == 'nan':
        allergies_default = []
    else:
        allergies_selected = user_info.allergies.values[0]
        allergies_default = [x.title() for x in allergies_selected.split(", ")]

    allergies = st.multiselect("Any allergies?", tuple(allergy for allergy in ALLERGIES), allergies_default)
    st.write(' ')

    if str(user_info.dislikes.values[0]) == 'nan':
        dislikes_default = []
    else:
        dislikes_selected = user_info.dislikes.values[0]
        dislikes_default = [x.title() for x in dislikes_selected.split(", ")]

    dislikes = st.multiselect("How about dislikes?", tuple(dislike for dislike in DISLIKES), dislikes_default)
    st.write(' ')

    if str(user_info.custom_dsl.values[0]) == 'nan':
        custom_dsl_default = ''
    else:
        custom_dsl_default = user_info.custom_dsl.values[0].title()

    custom_dsl = st.text_input("Any other dislikes?", value=custom_dsl_default)
    st.write(' ')

    if str(user_info.collab.values[0]) == 'nan':
        collab_default = 0.5
    else:
        collab_default = float(user_info.collab.values[0])

    collab = st.slider("Do you want to taste new recipes?", 0, 10, int(collab_default * 10))
    st.write(' ')

    # else:
    #     name = st.text_input("What is your name?")
    #     st.write(' ')
    #     diet = st.selectbox("Pick your diet:", tuple(diet for diet in LIST_DIET))
    #     st.write(' ')
    #     goal = st.selectbox("Pick your nutritional goal:", tuple(goal for goal in LIST_GOAL))
    #     st.write(' ')
    #     allergies = st.multiselect("Any allergies?", tuple(allergy for allergy in ALLERGIES))
    #     st.write(' ')
    #     dislikes = st.multiselect("How about dislikes?", tuple(dislike for dislike in DISLIKES))
    #     st.write(' ')
    #     custom_dsl = st.text_input("Any other dislikes?")
    #     st.write(' ')


    if st.button('✅ Save'):

        form = {'name': name.title(),
                'diet': diet.lower(),
                'goal': goal.lower(),
                'allergies': (', ').join(allergies).lower(),
                'dislikes': (', ').join(dislikes).lower(),
                'custom_dsl': custom_dsl.lower(),
                'collab': float(collab)/10}

        storage.save_prefs(app, form=form)
