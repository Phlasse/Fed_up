import streamlit as st
import pandas as pd
from PIL import Image

LIST_DIET = ['Classic', 'Low-Carb', 'Pescetarian', 'Vegetarian', 'Vegan']

LIST_GOAL = ['Maintain Weight','Lose Weight','Gain Weight','Build Muscles']

ALLERGIES = ['None','Milk','Eggs','Fish','Shellfish','Tree Nuts','Peanuts','Wheat','Soybeans','Mustard']

DISLIKES = {
    'Beets': ['beet'],
    'Bell peppers': ['bell pepper'],
    'Blue cheese': ['blue cheese'],
    'Brussels sprouts': ['brussels sprout'],
    'Cauliflower': ['cauliflower'],
    'Eggs': ['eggs'],
    'Goat cheese': ['goat cheese'],
    'Mushrooms': ['mushroom'],
    'Olives':['olive'],
    'Quinoa':['quinoa'],
    'Shrimp':['shrimp'],
    'Tofu':['tofu'],
    'Turnips':['turnip']
}

# def save_like(user_prefs, user_id, rid, liked):
#     user_prefs = pd.read_csv("app/data/user_prefs.csv")
#     user_prefs = user_prefs.append({'app_user_id': user_id, 'recipe_id': rid, 'liked': liked}, ignore_index=True)
#     user_prefs.to_csv("app/data/user_prefs.csv", index=False)


def main():

    ## Image background
    page_bg_img = '''
    <style>
    body {
        background-image: url("https://cdn.pixabay.com/photo/2017/06/06/22/46/mediterranean-cuisine-2378758_1280.jpg");
        background-size: cover;
        }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)


    menu = ["My account","Get Recommendations"]
    choice = st.selectbox("Select",menu)


    # Log in to your account
    if choice == "My account":
        st.markdown("<h3 style='text-align: justified; color: white;'>Define your personal preferences.</h3>", unsafe_allow_html=True)

        diet = st.selectbox("Pick your diet", tuple(diet for diet in LIST_DIET))
        allergies = st.multiselect("Any allergies?", tuple(allergy for allergy in ALLERGIES))
        dislikes = st.multiselect("How about dislikes?", tuple(dislike for dislike in DISLIKES))
        cst_dislikes = st.text_input("Any other dislikes? Write all the aliments you don't like.")
        goal = st.selectbox("Pick your nutritional goal", tuple(goal for goal in LIST_GOAL))



    # Create an account
    elif choice == "Get Recommendations":
        st.markdown("<h3 style='text-align: justified; color: white;'>TO LINK WITH PHILLIP'S CODE.</h3>", unsafe_allow_html=True)


if __name__ == '__main__':
    main()
