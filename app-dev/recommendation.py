import pandas as pd
import streamlit as st
import base64
from PIL import Image
from io import BytesIO
import requests
import Fed_up.filters
from fpdf import fpdf
import os
from datetime import datetime, timedelta
import streamlit.components.v1 as components
#from StringIO import StringIO

WIDTH= 215.9
HEIGHT = 279.4

@st.cache
def load_result():
    data = pd.read_csv("Fed_up/data/samples/my_sample.csv")
    return data


def recommendation(data):

    ### color = st.color_picker('Pick A Color', '#95D6A4')
    img_fed_up = Image.open("Fed_up/data/samples/logo.png")
    img_fed_up_sidebar = Image.open("Fed_up/data/samples/sidebar_logo.png")
    st.image(img_fed_up, width=200)
    st.sidebar.image(img_fed_up_sidebar, width=200)

    st.sidebar.markdown("# Here are your results!")
    st.sidebar.markdown("#### Feel free to adjust your search.")
    st.sidebar.markdown("    ")

    time = st.sidebar.slider("How patient are you today? (Minutes)", 15, 120, 60)
    steps = st.sidebar.slider("Define complexity? (steps)", 3, 20, 7)
    n_ingreds = st.sidebar.slider("How many different ingredients do you want?", 3, 25, 13)
    persons = st.sidebar.slider("For how many are you cooking?", 1, 20, 2)

    number_recipes = st.sidebar.slider("Number of recipes to show", 5, 40, 5)



    filtered_df = data[data.minutes<time]
    filtered_df = filtered_df[filtered_df.minutes>10]
    filtered_df = filtered_df[filtered_df.n_steps<steps]
    filtered_df = filtered_df[filtered_df.n_ingredients<n_ingreds]



### List of recipe recommendations on main window here ###
    recipes_picked = {}
    headers = [i for i in filtered_df["name"]]
    ingredients = [i.split("',") for i in filtered_df["ingredients"]]
    steps_todo = [i.split("',") for i in filtered_df["steps"]]
    urls = [i for i in filtered_df["image_url"]]
    rating_avg = [i for i in filtered_df["rating_mean"]]
    rating_qty = [i for i in filtered_df["rating_count"]]
    minutes_list = [i for i in filtered_df["minutes"]]
    calories = [int(i) for i in filtered_df["calories"]]
    total_fat = [i for i in filtered_df["total_fat"]]
    saturated_fat = [i for i in filtered_df["saturated_fat"]]
    sugar = [i for i in filtered_df["sugar"]]
    sodium = [i for i in filtered_df["sodium"]]
    protein = [i for i in filtered_df["protein"]]
    carbs = [i for i in filtered_df["carbohydrates"]]
    summed_ingredients = {}


    for i in range(number_recipes):
        st.header(headers[i].replace(" s ", "'s ").upper())
        response_pic = requests.get(urls[i])#"https://cdn.pixabay.com/photo/2017/06/01/18/46/cook-2364221_1280.jpg")
        img = Image.open(BytesIO(response_pic.content))
        st.image(img, width=697)

        check, minutes, rating=st.beta_columns(3)
        with check:
            check_box = st.checkbox(f'Add no. {i+1} to selection')
            if check_box:
                recipes_picked[f'{i+1}'] = 1
            else:
                recipes_picked[f'{i+1}'] = 0
        with minutes:
            st.write(f'{int(minutes_list[i])} minutes to prepare')
        with rating:
            st.write(f'{round(float(rating_avg[i]),2)} Stars on {int(rating_qty[i])} reviews.')
        pic, ing, steps=st.beta_columns(3)
        with pic:

            st.subheader("Stats:")
            st.write(f'Calories: {calories[i]} Cal')
            st.write(f'Total fat: {total_fat[i]} %*')
            st.write(f'Saturated fat: {saturated_fat[i]} %*')
            st.write(f'Sugar: {sugar[i]} %*')
            st.write(f'Sodium: {sodium[i]} %*')
            st.write(f'Protein: {protein[i]} %*')
            st.write(f'Carbohydrates: {carbs[i]} %*')

        with ing:
            st.subheader('Ingredient:')

            for j in ingredients[i]:
                ji = j.replace("[", "").replace("]", "").replace("'", "")
                st.write(ji.capitalize())
                if recipes_picked[f'{i+1}'] == 1:
                    if ji in summed_ingredients:
                        summed_ingredients[ji] += 1*persons
                    else:
                        summed_ingredients[ji] = 1*persons

        with steps:
            st.subheader('Directions::')
            for index, step in enumerate(steps_todo[i]):
                step = step.replace("[", "").replace("]", "").replace("'","")
                st.write(f'{index+1}: {step.capitalize()}')

    st.sidebar.subheader("Your selection:")
    for i in range(len(recipes_picked)):
        if recipes_picked[f'{i+1}'] ==1:
            st.sidebar.write(headers[i].replace(" s ", "'s ").capitalize())
    st.sidebar.subheader("Complete ingredient List:")
    for key, value in summed_ingredients.items():
        st.sidebar.write(value, " x ", key)


    st.write("\* refers to the average person with a calorie intake of 2000 calories per day.")

    ing_list_exp = pd.DataFrame()
    ing_list_exp["quantity"] = list(summed_ingredients.values())
    ing_list_exp["Ingredient"] = list(summed_ingredients.keys())

    txt = ing_list_exp.to_csv(index = False)
    b64 = base64.b64encode(txt.encode()).decode()
    href = f'<a href="data:file/ingredients.txt;base64,{b64}">Download Ingredient List</a> (right-click and save as &lt;some_name&gt;.txt)'
    st.sidebar.markdown(href, unsafe_allow_html=True)

    #### DF can be printed with comment line below ####
    #st.write(filtered_df.head(5))

    return

def export_to_pdf(Selection, df):
    pdf = FPDF()
    pdf.output("what")

    return

if __name__=="__main__":
    #set_background()
    results = load_result()
    recommendation(results)
