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

    # Homepage: Text content
    st.markdown("<h1 style='text-align: justified; color: black;'>Welcome to Fed Up!</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: justified; color: black;'>Fed up! provides you with personalized meal recommendations based on your food preferences and personal diet plan.</h3>", unsafe_allow_html=True)
    st.markdown("---")


    st.markdown("<h2 style='text-align: justified; text-decoration: underline; color: black;'>How does it work?</h2>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown("<span style='text-align: justified; color: black;'> 1️⃣ ~ Define your food preferences and nutritional goal. 👨🏻‍🍳 👩🏽‍🍳</span>", unsafe_allow_html=True)
    st.markdown("<span style='text-align: justified; color: black;'> 2️⃣ ~ Fed Up! recommends you tonight’s dinner or a meal plan for the entire next week. 🥗 🍣 </span>", unsafe_allow_html=True)
    st.markdown("<span style='text-align: justified; color: black;'> 3️⃣ ~ Fed up! creates a shopping list based on your meals and automatically adds it to your Microsoft To Do grocery list. 📲 🛒</span>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: justified; color: black;'> </h1>", unsafe_allow_html=True)


    menu = ["Log in","Sign up"]
    choice = st.selectbox("Log in or sign up",menu)

    # Log in to your account
    if choice == "Log in":
        st.markdown("<h2 style='text-align: justified; font-weight: bold; color: black;'>Login to your account</h2>", unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password",type='password')
        if st.checkbox("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:

                st.success("Logged In as {}".format(username))

            else:
                st.warning("Incorrect Username/Password")

    # Create an account
    elif choice == "Sign up":
        st.markdown("<h2 style='text-align: justified; font-weight: bold; color: black;'>Create your account</h2>", unsafe_allow_html=True)
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Sign up"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
