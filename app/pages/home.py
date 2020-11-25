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


def run(app):

    ## Homepage: image background
    page_bg_img = '''
    <style>
    body {
        background-image: url("https://cdn.pixabay.com/photo/2017/08/05/12/33/flat-lay-2583213_1280.jpg");
        background-size: cover;
        }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    whitespace, info = st.beta_columns([1, 3])
    # Homepage: Text content

    with info:
        st.markdown("<h1 style='text-align: justified; color: #78C2A4;'>Welcome to Fed Up!</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: justified; line-height: 1.2'>Fed Up! provides you with personalized meal recommendations based on your food <br>preferences and personal diet plan.</h3>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<h3 style='text-align: justified; color: #78C2A4'><strong>How does it work?</strong></h3>", unsafe_allow_html=True)
        st.markdown("")
        st.markdown("<span style='text-align: justified;'> 1️⃣ ~ Define your food preferences and nutritional goal. 👨🏻‍🍳 👩🏽‍🍳</span>", unsafe_allow_html=True)
        st.markdown("<span style='text-align: justified;'> 2️⃣ ~ Fed Up! recommends you tonight’s dinner or a meal plan for the entire next week. 🥗 🍣 </span>", unsafe_allow_html=True)
        st.markdown("<span style='text-align: justified;'> 3️⃣ ~ Fed Up! creates a shopping list based on your meals and adds it to your Microsoft To Do grocery list. 📲 🛒</span>", unsafe_allow_html=True)
