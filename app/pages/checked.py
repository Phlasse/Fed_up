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
from helpers import side_filters


def run(app):
    # Display headers
    st.write("# Checked Recipes")
    st.write(f"🏁 See the details of the recipes in your basked!")
    st.markdown("---")

    st.sidebar.markdown("---")

    checked_recipes = app.user_checkouts.sort_values(by='timestamp', ascending=False)
    data = checked_recipes.merge(app.recipes, on='recipe_id', how='inner')

    if len(data) > 0:
        for index, recipe in data.iterrows():
            draw_recipe(app, recipe, 'checked')
            st.markdown("---")

    else:
        st.markdown("###### *No checked recipes, try add items to your basket!*")
