import pandas as pd
import streamlit as st
import base64
from PIL import Image
from io import BytesIO
import requests
import Fed_up.filters
#from StringIO import StringIO



@st.cache
def load_result():
    data = pd.read_csv("Fed_up/data/samples/recipe_sample_20201118_1137.csv")
    return data


def recommendation(data):

    #set_background()
    st.sidebar.markdown("# Here are your results!")
    st.sidebar.markdown("#### Feel free to adjust your search.")
    st.sidebar.markdown("    ")

    time = st.sidebar.slider("How patient are you today? (Minutes)", 15, 120, 30)
    steps = st.sidebar.slider("Define complexity? (steps)", 1, 20, 7)

    filtered_df = data[data.minutes<time]
    filtered_df = filtered_df[filtered_df.n_steps<steps-1]


### List of recipe recommendations on main window here ###
    recipes_picked = {}
    headers = [i for i in filtered_df["name"]]
    ingredients = [i.split(",") for i in filtered_df["ingredients"]]
    steps_todo = [i.split(",") for i in filtered_df["steps"]]

    for i in range(5):
        st.header(headers[i].upper())
        pic, ing, steps=st.beta_columns(3)
        with pic:
            st.subheader('')
            response_pic = requests.get("https://cdn.pixabay.com/photo/2017/06/01/18/46/cook-2364221_1280.jpg")
            img = Image.open(BytesIO(response_pic.content))
            st.image(img, width=200)
            check_box = st.checkbox(f'Add no. {i}')
            if check_box:
                recipes_picked[f'{i}'] = 1
            else:
                recipes_picked[f'{i}'] = 0
        with ing:
            st.subheader('Ingredient:')

            #st.text(filtered_df[i:i+1].ingredients)
            for j in ingredients[i]:
                st.text(j.replace("[", "").replace("]", "").replace("'", ""))
        with steps:
            st.subheader('Directions::')
            #st.write(steps_todo[i])
            for index, step in enumerate(steps_todo[i]):
                st.write(f'{index+1}: {step.replace("[", "").replace("]", "")}')

    st.sidebar.subheader("Your selection:")
    for i in range(len(recipes_picked)):
        if recipes_picked[f'{i}'] ==1:
            st.sidebar.write(headers[i])


    #data = data[["name", "recipe_id", "minutes", ]]
    st.write(filtered_df.head(5))


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
    results = load_result()
    recommendation(results)
