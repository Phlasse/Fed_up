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
    filtered_df = filtered_df[filtered_df.n_steps<steps]

    #selected_recipes = {}
    #check_box = {}
    #for i in range(20):
    ##    st.subheader(filtered_df[i:i+1].name)
  #      pic, ing, dec, check=st.beta_columns(4)
     #   with pic:
      #      response_pic = requests.get("https://cdn.pixabay.com/photo/2017/06/01/18/46/cook-2364221_1280.jpg")
       #     img = Image.open(BytesIO(response_pic.content))
        #    st.image(img, width=150)
   #     with ing:
    #        st.text(filtered_df[i:i+1].ingredients)
     #   with dec:
     #       st.text("hi")#filtered_df.ingredients[i])
      #  with check:
       #     check_box[i] = st.checkbox('select')
        #    if check_box[i]:
         #       selected_recipes[i] = filtered_df[i:i+1].recipe_id


    #data = data[["name", "recipe_id", "minutes", ]]
    st.write(filtered_df.head(5))
    response = requests.get("https://cdn.pixabay.com/photo/2017/06/01/18/46/cook-2364221_1280.jpg")
    img = Image.open(BytesIO(response.content))
    #img = Image.open(StringIO(response.content))
    st.image(img, width=500)


    login, signin = st.sidebar.beta_columns(2)
    with login:
        member = st.button("Log in")

    with signin:
        new_user = st.button("New User")

    if new_user:
        username = st.sidebar.text_input("Username : ", "")
        st.sidebar.text("Select your allergies :")
        for allergy in ALLERGIES:
            st.sidebar.checkbox(allergy, value=False, key=allergy)

    if member:
        ### Manage stuff for existing users ###
        st.sidebar.selectbox("Select your username : ", ["Jessica", "Nuno", "Olivier", "Phillip"])






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
