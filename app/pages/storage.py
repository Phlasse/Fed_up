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


def save_prefs(app, form={}):
    info = app.prefs[(app.prefs.app_user_id == app.user_id)]

    if len(info) == 1:
        index = info.index[0]
        prefs = app.prefs
        prefs.loc[index, 'name'] = form['name']
        prefs.loc[index, 'diet'] = form['diet']
        prefs.loc[index, 'goal'] = form['goal']
        prefs.loc[index, 'allergies'] = form['allergies']
        prefs.loc[index, 'dislikes'] = form['dislikes']
        prefs.loc[index, 'custom_dsl'] = form['custom_dsl']
        prefs.loc[index, 'collab'] = form['collab']
        prefs.to_csv(app.prefs_path, index=False)
        st.success("Profile information saved!")


def save_like(app, rid, liked):
    info = app.likes[(app.likes.app_user_id == app.user_id) & (app.likes.recipe_id == rid)]

    if len(info) == 1:
        index = info.index[0]
        app.likes.loc[index, 'liked'] = liked
        app.likes.loc[index, 'timestamp'] = pd.Timestamp.now()
    else:
        app.likes = app.likes.append({'app_user_id': app.user_id, 'recipe_id': rid, 'liked': liked, 'timestamp': pd.Timestamp.now()}, ignore_index=True)

    app.likes.to_csv(app.likes_path, index=False)


def clear_like(app, rid):
    info = app.likes[(app.likes.app_user_id == app.user_id) & (app.likes.recipe_id == rid)]

    if len(info) == 1:
        index = info.index[0]
        app.likes.drop(app.likes.index[index], inplace=True)
        app.likes.to_csv(app.likes_path, index=False)


def add_to_checkout(app, rid):
    info = app.checkouts[(app.checkouts.app_user_id == app.user_id) & (app.checkouts.recipe_id == rid)]

    if len(info) < 1:
        app.checkouts = app.checkouts.append({'app_user_id': app.user_id, 'recipe_id': rid, 'timestamp': pd.Timestamp.now()}, ignore_index=True)
        app.checkouts.to_csv(app.checkouts_path, index=False)


def remove_from_checkout(app, rid):
    info = app.checkouts[(app.checkouts.app_user_id == app.user_id) & (app.checkouts.recipe_id == rid)]

    if len(info) == 1:
        index = info.index[0]
        app.checkouts.drop(app.checkouts.index[index], inplace=True)
        app.checkouts.to_csv(app.checkouts_path, index=False)


def add_to_checkout(app, rid):
    info = app.checkouts[(app.checkouts.app_user_id == app.user_id) & (app.checkouts.recipe_id == rid)]

    if len(info) < 1:
        app.checkouts = app.checkouts.append({'app_user_id': app.user_id, 'recipe_id': rid, 'timestamp': pd.Timestamp.now()}, ignore_index=True)
        app.checkouts.to_csv(app.checkouts_path, index=False)
