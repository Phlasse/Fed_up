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
from google.cloud import storage
from google.oauth2 import service_account
import json
import _cffi_backend as backend


import home
import preferences
import roulette
import recommendation
import liked
import dashboard
import checkout


CSS = """
    img {
        border-radius: 4px;
    }

    .stProgress .st-ep { background: linear-gradient(135deg, rgba(149,214,164,1) 0%, rgba(1,85,98,1) 100%); }
"""

st.set_page_config(page_title='FedUp', page_icon="🍲", layout='centered', initial_sidebar_state='collapsed')
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

BUCKET_NAME = "fed-up-bucket-01"
PROJECT_ID = "fed-up-2020"


#@st.cache(show_spinner=False)
def load_inputs(recipes_path, content_matrix_path, rating_matrix_path, creds=''):
    #if creds:
    client = storage.Client()
    recipes = pd.read_csv(recipes_path)
    content_matrix = pd.read_csv(content_matrix_path).rename(columns={'Unnamed: 0': 'recipe_id'}).set_index('recipe_id')
    rating_matrix = pd.read_csv(rating_matrix_path).rename(columns={'Unnamed: 0': 'recipe_id'}).set_index('recipe_id')
    return recipes, content_matrix, rating_matrix


#@st.cache(show_spinner=False)
# def get_credentials():
#     credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
#     if '.json' in credentials_raw:
#         credentials_raw = open(credentials_raw).read()
#     credentials_raw = credentials_raw.replace("\\n","")
#     creds_json = json.loads(credentials_raw)
#     creds_gcp = service_account.Credentials.from_service_account_info(creds_json)
#     return creds_gcp


class MultiApp:

    def __init__(self, local=False):

        self.apps = []

        self.user_id = 3

        if local:
            self.local = True
            self.recipes_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/recipe_pp.csv"))
            self.prefs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_prefs.csv"))
            self.likes_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_likes.csv"))
            self.checkouts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_checkouts.csv"))
            self.content_matrix_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/content_latent.csv"))
            self.rating_matrix_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/rating_latent.csv"))
            self.creds = ''
        else:
            self.local = False
            self.recipes_path = f"gs://fed-up-bucket-01/data/app/recipe_pp.csv"
            self.prefs_path = f"gs://fed-up-bucket-01/data/app/user_prefs.csv"
            self.likes_path = f"gs://fed-up-bucket-01/data/app/recipe_pp.csv"
            self.checkouts_path = f"gs://fed-up-bucket-01/data/app/user_checkouts.csv"
            self.content_matrix_path = f"gs://fed-up-bucket-01/data/app/content_latent.csv"
            self.rating_matrix_path = f"gs://fed-up-bucket-01/data/app/rating_latent.csv"
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

    # Start app
    app = MultiApp()

    # Add pages
    app.add_app("Home", home.run)
    app.add_app("Profile", preferences.run)
    app.add_app("Food Roulette", roulette.run)
    app.add_app("Recommendations", recommendation.run)
    app.add_app("Liked Recipes", liked.run)
    # app.add_app("Dashboard", dashboard.run)
    app.add_app("Checkout", checkout.run)

    # Run the app
    app.run()

    # Loading data
    # app.load_static_data()
    # app.load_basic_data()
    # app.load_user_data()
