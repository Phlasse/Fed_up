import pandas as pd
import streamlit as st
import base64
from PIL import Image
from io import BytesIO
import requests

from Fed_up import filters

@st.cache
def load_result():
    user_id = 1
    data = pd.read_csv("Fed_up/data/samples/recipe_sample.csv")
    tinder_data = data[data['rating_count'] > 5].sort_values(by='rating_mean', ascending=False)
    user_prefs = pd.read_csv("app/data/user_prefs.csv")
    user = user_prefs[user_prefs.app_user_id == user_id] ### Replace by user id
    user_data = filters.all_filters(tinder_data, goal = user['goal'].values[0],
                                                 diet = user['diet'].values[0],
                                                 allergies = user['allergies'].values[0].split(", "),
                                                 dislikes = user['dislikes'].values[0].split(", "),
                                                 custom_dsl = user['custom_dsl'].values[0])

    print(f"User #{user['app_user_id'].values[0]} - {user['name'].values[0]}: {len(tinder_data)} > {len(user_data)}")

    return user_data, user


def foodinder(data, user):
    # Get user info
    user_id = user['app_user_id'].values[0]
    user_fname = user['name'].values[0].split(" ")[0]

    # Display headers
    st.write("# Food Roulette")
    st.write(f"#### Tell us what you like, {user_fname}!")
    st.write("")

    # Select next item
    user_recipes = pd.read_csv("app/data/user_likes.csv")
    rated_recipes = user_recipes[user_recipes.app_user_id == user_id].recipe_id.values
    roulette_data = data[~(data['recipe_id'].isin(rated_recipes))]
    next_item = roulette_data.head(1)

    # Display next item



    return


def set_background():
    page_bg_img = '''
    <style>
    body {
        background-image: url("https://cdn.pixabay.com/photo/2017/06/01/18/46/cook-2364221_1280.jpg");
        background-size: cover;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


if __name__=="__main__":
    #set_background()
    results, user = load_result()
    foodinder(results, user)
