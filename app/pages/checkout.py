import pandas as pd
import numpy as np
import seaborn as sns

import streamlit as st
import streamlit.components.v1 as components

import base64
from PIL import Image
from io import BytesIO
import requests
import time
import os


ADJUSTED_LIST = ['olive oil', 'salt', 'pepper', 'cayenne', 'salt and pepper', 'garlic salt', 'butter', 'garlic cloves', 'black pepper', 'fresh rosemary', 'garlic clove','kosher salt', 'rosemary', 'oil', 'salt & freshly ground black pepper', 'ground black pepper', 'sugar']

def run(app):
    # Display headers
    st.write("# Checkout")
    st.write(f"🛒 Confirm and export your selected dishes.")
    st.markdown("---")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Actions")
    st.sidebar.markdown("    ")

    ckouts = app.user_checkouts.merge(app.recipes, on="recipe_id", how="left")

    if len(ckouts) == 0:
        st.markdown("###### *No delicious recipes added to the checkout yet!*")

    else:
        st.write("### **SELECTED RECIPES:**")
        st.write(' ')

        data_cols = ['calories', 'total_fat', 'saturated_fat', 'sugar', 'sodium', 'protein', 'carbohydrates']
        recipes_show = ckouts[data_cols]
        recipes_show['name'] = ckouts.copy()['name'].str.title()
        recipes_show[data_cols] = recipes_show[data_cols].astype(int)
        recipes_show = recipes_show.set_index('name') \
                                    .rename(columns={'name': 'Name', 'calories': 'Calories',
                                        'total_fat': 'Total fat', 'saturated_fat': "Saturated fat",
                                        'sugar': 'Sugar', 'sodium': 'Sodium', 'protein': 'Protein',
                                        'carbohydrates': 'Carbs'})

        st.table(recipes_show.style.background_gradient(cmap ='Greens', axis=0))

        st.write(f'###### *Calories in Cal; other figures as % for a daily intake of 2000 calories*')

        st.markdown("---")
        st.write("### **GROCERY LIST:**")
        st.write(' ')

        ingredient_show, _space = st.beta_columns([1, 1])

        with ingredient_show:
            ingredients = ckouts[['ingredients']]
            summed_ingredients = {}

            for index, row in ingredients.iterrows():
                ings = eval(row['ingredients'])

                for ing in ings:
                    if ing in summed_ingredients.keys():
                        summed_ingredients[ing] += 1
                    else:
                        summed_ingredients[ing] = 1

            ing_list_exp = pd.DataFrame()
            ing_list_exp["Ingredient"] = list(summed_ingredients.keys())
            ing_list_exp["Quantity"] = list(summed_ingredients.values())
            ing_list_exp = ing_list_exp[~(ing_list_exp.Ingredient.isin(ADJUSTED_LIST))]
            ing_list_exp["Ingredient"] = ing_list_exp["Ingredient"].str.title()
            ing_list_exp = ing_list_exp.set_index('Ingredient').sort_values(by="Quantity", ascending=False)

            st.table(ing_list_exp.style.background_gradient(cmap ='Greens', axis=0))


    #btn = st.sidebar.button("📝 Export to Microsoft To Do")
    #if btn:
    #    for key, value in summed_ingredients.items():
    #        time.sleep(0.25)
    #        call_url = f"https://hook.integromat.com/5oboi86rrbc1qsf5koeulfmtwn76c9qg?Subject={key}%20{value}%20x&note=Subscribe%20to%20Fed-up&list=Fed-up"
    #        call = requests.get(call_url)

    btn2 = st.sidebar.button("🚗 Batch #469 Done!")
    if btn2:
        st.balloons()


        ###########################
        ### weird export option ###
        ###########################
        # txt = ing_list_exp.to_csv(index = False)
        # b64 = base64.b64encode(txt.encode()).decode()
        # href = f'<a href="data:file/ingredients.txt;base64,{b64}">Download</a> (right-click and save as Grocery.txt)'
        # st.markdown(href, unsafe_allow_html=True)
        # st.table(ing_list_exp)

