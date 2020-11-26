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
import time
import os

import sys
import argparse

from google.cloud import storage
from google.oauth2 import service_account
import json

import home
import preferences
import roulette
import recommendation
import liked
import checked
import checkout


CSS = """
    img {border-radius: 4px;}
    .stProgress > div > div > div { background: linear-gradient(135deg, #95D6A4 0%, #78C2A4 100%); }
    table {font-family: "IBM Plex Sans", sans-serif;}
"""

st.set_page_config(page_title='Fed Up!', page_icon="🍲", layout='centered')
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

BUCKET_NAME = "fed-up-bucket-01"
PROJECT_ID = "fed-up-2020"


@st.cache(show_spinner=False)
def load_inputs(recipes_path, content_matrix_path, rating_matrix_path, creds=''):
    recipes = pd.read_csv(recipes_path)
    content_matrix = pd.read_csv(content_matrix_path).rename(columns={'Unnamed: 0': 'recipe_id'}).set_index('recipe_id')
    rating_matrix = pd.read_csv(rating_matrix_path).rename(columns={'Unnamed: 0': 'recipe_id'}).set_index('recipe_id')
    return recipes, content_matrix, rating_matrix


class MultiApp:

    def __init__(self, local=True):
        self.local = local
        self.apps = []
        self.user_id = 5

        if self.local:
            self.recipes_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/recipe_pp.csv"))
            self.prefs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_prefs.csv"))
            self.likes_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_likes.csv"))
            self.checkouts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_checkouts.csv"))
            self.content_matrix_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/content_latent.csv"))
            self.rating_matrix_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/rating_latent.csv"))
            self.creds = ''
        else:
            self.recipes_path = f"https://storage.googleapis.com/fed-up-bucket-01/data/app/recipe_pp.csv"
            self.prefs_path = f"https://storage.googleapis.com/fed-up-bucket-01/data/app/user_prefs.csv"
            self.likes_path = f"https://storage.googleapis.com/fed-up-bucket-01/data/app/user_likes.csv"
            self.checkouts_path = f"https://storage.googleapis.com/fed-up-bucket-01/data/app/user_checkouts.csv"
            self.content_matrix_path = f"https://storage.googleapis.com/fed-up-bucket-01/data/app/content_latent.csv"
            self.rating_matrix_path = f"https://storage.googleapis.com/fed-up-bucket-01/data/app/rating_latent.csv"
            self.creds = ''

        self.load_static_data()
        self.load_basic_data()
        self.load_user_data()


    def load_static_data(self):
        recipes, content_matrix, rating_matrix = load_inputs(self.recipes_path, self.content_matrix_path, self.rating_matrix_path, creds=self.creds)
        self.recipes = recipes
        self.content_matrix = content_matrix
        self.rating_matrix = rating_matrix


    def load_basic_data(self):
        self.prefs = pd.read_csv(self.prefs_path)
        self.likes = pd.read_csv(self.likes_path)
        self.checkouts = pd.read_csv(self.checkouts_path)


    def load_user_data(self):
        self.user_prefs = self.prefs[self.prefs.app_user_id == self.user_id]
        self.user_name = self.user_prefs.name.values[0]
        self.user_rates = self.likes[(self.likes.app_user_id == self.user_id)]
        self.user_likes = self.user_rates[(self.user_rates.liked == 1)]
        self.user_dislikes = self.user_rates[(self.user_rates.liked == 0)]
        self.user_checkouts = self.checkouts[(self.checkouts.app_user_id == self.user_id)]


    def set_time(self, time):
        self.time = time

    def get_time(self):
        if 'time' in locals():
            return self.time
        else:
            return 60


    def set_steps(self, steps):
        self.steps = steps

    def get_steps(self):
        if 'steps' in locals():
            return self.steps
        else:
            return 7


    def set_ingreds(self, ingreds):
        self.ingreds = ingreds

    def get_ingreds(self):
        if 'ingreds' in locals():
            return self.ingreds
        else:
            return 10


    def set_n_recipes(self, n_recipes):
        self.n_recipes = n_recipes

    def get_n_recipes(self):
        if 'n_recipes' in locals():
            return self.n_recipes
        else:
            return 5


    def set_recs(self, recs):
        self.recs = recs

    def get_recs(self):
        if 'recs' in locals():
            return self.recs
        else:
            return None


    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })


    def run(self):
        logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets/sidebar_logo.png")) # TO DO: DEFINE PROPER PATH
        img_fed_up = Image.open(logo_path)
        st.sidebar.image(img_fed_up, width=180)

        app = st.sidebar.radio(
            ' ',
            self.apps,
            format_func=lambda app: app['title'])

        app['function'](self)


if __name__ == "__main__":

    # Getting args
    parser = argparse.ArgumentParser()
    parser.add_argument('--local', action='store', dest='local',
                        help='Flag for Debug mode', default=True)
    args = parser.parse_args()

    # Start app
    app = MultiApp(args.local)

    # Add pages
    app.add_app("Home", home.run)
    app.add_app("Profile", preferences.run)
    app.add_app("Food Roulette", roulette.run)
    app.add_app("Recommendations", recommendation.run)
    app.add_app("Liked Recipes", liked.run)
    app.add_app("Checked Recipes", checked.run)
    app.add_app("Checkout", checkout.run)

    # Run the app
    app.run()
