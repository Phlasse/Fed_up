"""Frameworks for running multiple Streamlit applications as a single app.
"""
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

import preferences
import roulette
import recommendation
import liked
import checkout
import dashboard


CSS = """
"""

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

# img_fed_up = Image.open("Fed_up/data/samples/logo.png")
# img_fed_up_sidebar = Image.open("Fed_up/data/samples/sidebar_logo.png")
# st.sidebar.image(img_fed_up_sidebar, width=200)


class MultiApp:

    def __init__(self):
        self.apps = []

        self.user_id = 3

        self.recipes_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "Fed_up/data/samples/recipe_sample.csv")) # TO DO: DEFINE PROPER PATH
        self.recipes = pd.read_csv(self.recipes_path)

        self.prefs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_prefs.csv")) # TO DO: DEFINE PROPER PATH
        self.prefs = pd.read_csv(self.prefs_path)
        self.user_prefs = self.prefs[self.prefs.app_user_id == self.user_id]

        self.user_name = self.user_prefs.name.values[0]

        self.likes_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_likes.csv")) # TO DO: DEFINE PROPER PATH
        self.likes = pd.read_csv(self.likes_path)

        self.user_rates = self.likes[(self.likes.app_user_id == self.user_id)]
        self.user_likes = self.user_rates[(self.user_rates.liked == 1)]
        self.user_dislikes = self.user_rates[(self.user_rates.liked == 0)]

        self.checkouts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_checkouts.csv")) # TO DO: DEFINE PROPER PATH
        self.checkouts = pd.read_csv(self.checkouts_path)
        self.user_checkouts = self.checkouts[(self.checkouts.app_user_id == self.user_id)]


    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })


    def run(self):
        logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets/sidebar_logo.png")) # TO DO: DEFINE PROPER PATH
        img_fed_up = Image.open(logo_path)
        st.sidebar.image(img_fed_up, width=150)

        app = st.sidebar.radio(
            ' ',
            self.apps,
            format_func=lambda app: app['title'])

        app['function'](self)


if __name__ == "__main__":

    app = MultiApp()
    app.add_app("Profile", preferences.run)
    app.add_app("Food Roulette", roulette.run)
    app.add_app("Recommendations", recommendation.run)
    app.add_app("Liked Recipes", liked.run)
    app.add_app("Checkout", checkout.run)
    app.add_app("Dashboard", dashboard.run)
    app.run()
