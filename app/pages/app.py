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

st.set_page_config(page_title='FedUp', page_icon="🍲", layout='centered', initial_sidebar_state='collapsed')
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)


@st.cache(suppress_st_warning=True)
def load_matrices(recipes_path, content_matrix_path, rating_matrix_path):
    recipes = pd.read_csv(recipes_path)
    content_matrix = pd.read_csv(content_matrix_path).rename(columns={'Unnamed: 0': 'recipe_id'}).set_index('recipe_id')
    rating_matrix = pd.read_csv(rating_matrix_path).rename(columns={'Unnamed: 0': 'recipe_id'}).set_index('recipe_id')
    return recipes, content_matrix, rating_matrix


class MultiApp:

    def __init__(self):

        self.apps = []

        self.user_id = 3

        # TO DO: DEFINE PROPER PATH
        self.recipes_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/recipe_pp.csv"))
        self.prefs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_prefs.csv"))
        self.likes_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_likes.csv"))
        self.checkouts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/user_checkouts.csv"))
        self.content_matrix_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/content_latent.csv"))
        self.rating_matrix_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data/rating_latent.csv"))

        self.prefs = pd.read_csv(self.prefs_path)
        self.likes = pd.read_csv(self.likes_path)
        self.checkouts = pd.read_csv(self.checkouts_path)

        recipes, content_matrix, rating_matrix = load_matrices(self.recipes_path, self.content_matrix_path, self.rating_matrix_path)
        self.recipes = recipes
        self.content_matrix = content_matrix
        self.rating_matrix = rating_matrix

        self.user_prefs = self.prefs[self.prefs.app_user_id == self.user_id]
        self.user_name = self.user_prefs.name.values[0]
        self.user_rates = self.likes[(self.likes.app_user_id == self.user_id)]
        self.user_likes = self.user_rates[(self.user_rates.liked == 1)]
        self.user_dislikes = self.user_rates[(self.user_rates.liked == 0)]
        self.user_checkouts = self.checkouts[(self.checkouts.app_user_id == self.user_id)]


    # def heavy_load(self):
    #     recipes, content_matrix, rating_matrix = load_matrices(self.recipes_path, self.content_matrix_path, self.rating_matrix_path)
    #     self.recipes = recipes
    #     self.content_matrix = content_matrix
    #     self.rating_matrix = rating_matrix


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

    app = MultiApp()
    app.add_app("Profile", preferences.run)
    app.add_app("Food Roulette", roulette.run)
    app.add_app("Recommendations", recommendation.run)
    app.add_app("Liked Recipes", liked.run)
    app.add_app("Checkout", checkout.run)
    # app.add_app("Dashboard", dashboard.run)
    app.run()
    # app.heavy_load()
