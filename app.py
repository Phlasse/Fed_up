## APP / Front End File ##

from datetime import datetime

import joblib
import pandas as pd
import pytz
import streamlit as st
import base64
#   from Fed_up.filters import *




ALLERGIES = ['milk','eggs','fish','shellfish','tree_nuts','peanuts','wheat','soybeans','mustard']



# @st.cache
# Define a function to load the DataFrames (recipe, review, users) below @st.cache
#def load_dataframe():
    #recipe_df = pd.read_csv(path_to_csv_file_in_cloud)
    #review_df = pd.read_csv(path_to_csv_file_in_cloud)
    #users_df = pd.read_csv(path_to_csv_file_in_cloud)
    #return recipe_df, review_df, users_df

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()




def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

### Running Cache data HERE ###


# def read_data(n_rows=10000):
#     df = get_data(n_rows=n_rows, local=False)
#     return df


# def format_input(pickup, dropoff, passengers=1):
#     pickup_datetime = datetime.utcnow().replace(tzinfo=pytz.timezone('America/New_York'))
#     formated_input = {
#         "pickup_latitude": pickup["latitude"],
#         "pickup_longitude": pickup["longitude"],
#         "dropoff_latitude": dropoff["latitude"],
#         "dropoff_longitude": dropoff["longitude"],
#         "passenger_count": passengers,
#         "pickup_datetime": str(pickup_datetime),
#         "key": str(pickup_datetime)}
#     return formated_input


def main():


    background = "Fed_up/data/images/kitchen_background.jpg" ## Set path to image background here.
    set_png_as_page_bg(background)

    # Load Data DataFrame here :
    # recipe_df, review_df, users_df = load_dataframe()

    st.sidebar.markdown("## Hey ! Welcome to Fed Up :)")

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





    # if analysis == "Dataviz":
    #     st.header("TaxiFare Basic Data Visualisation")
    #     st.markdown("**Have fun immplementing your own Taxifare Dataviz**")

    # if analysis == "prediction":
    #     #pipeline = joblib.load('data/model.joblib')
    #     #print("loaded model")
    #     st.header("TaxiFare Model predictions")
    #     # inputs from user
    #     pickup_adress = st.text_input("pickup adress", "251 Church St, New York, NY 10013")
    #     dropoff_adress = st.text_input("dropoff adress", "434 6th Ave, New York, NY 10011")
    #     # Get coords from input adresses usung HERE geocoder
    #     #pickup_coords = geocoder_here(pickup_adress)
    #     #dropoff_coords = geocoder_here(dropoff_adress)
    #     # inputs from user
    #     passenger_counts = st.selectbox("# passengers", [1, 2, 3, 4, 5, 6], 1)
    #     data = pd.DataFrame([pickup_coords, dropoff_coords])
    #     to_predict = [format_input(pickup=pickup_coords, dropoff=dropoff_coords, passengers=passenger_counts)]
    #     X = pd.DataFrame(to_predict)
    #     #res = pipeline.predict(X[COLS])
    #     #st.write("💸 taxi fare", res[0])
    #     st.map(data=data)


# print(colored(proc.sf_query, "blue"))
# proc.test_execute()
if __name__ == "__main__":
    #df = read_data()
    main()
