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


def side_filters(app):

    search = st.sidebar.text_input("Search by keyword:")

    time = st.sidebar.slider("How long are you willing to wait?", 15, 180, app.get_time())
    app.set_time(time)

    steps = st.sidebar.slider("How many steps are you willing to execute?", 3, 20, app.get_steps())
    app.set_steps(steps)

    ingreds = st.sidebar.slider("How many ingredients are you willing to use?", 3, 25, app.get_ingreds())
    app.set_ingreds(ingreds)

    n_recipes = st.sidebar.slider("How many dishes do you want to see?", 5, 40, app.get_n_recipes())
    app.set_n_recipes(n_recipes)

    return search, time, steps, ingreds, n_recipes


def clean_prefs(prefs):
    if str(prefs['goal'].values[0]) != 'nan':
        goal = prefs['goal'].values[0]
    else:
        goal = ''

    if str(prefs['diet'].values[0]) != 'nan':
        diet = prefs['diet'].values[0]
    else:
        diet = ''

    if str(prefs['allergies'].values[0]) != 'nan':
        allergies = prefs['allergies'].values[0].split(", "),
    else:
        allergies = []

    if str(prefs['dislikes'].values[0]) != 'nan':
        dislikes = prefs['dislikes'].values[0].split(", "),
    else:
        dislikes = []

    if str(prefs['custom_dsl'].values[0]) != 'nan':
        custom_dsl = prefs['custom_dsl'].values[0]
    else:
        custom_dsl = ''

    return goal, diet, allergies, dislikes, custom_dsl
