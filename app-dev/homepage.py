import streamlit as st
import pandas as pd


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data



def main():

    ## Homepage: image background
    page_bg_img = '''
    <style>
    body {
        background-image: url("https://cdn.pixabay.com/photo/2017/06/06/22/46/mediterranean-cuisine-2378758_1280.jpg");
        background-size: cover;
        }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Homepage: Text content
    st.markdown("<h1 style='text-align: justified; color: white;'>Welcome to Fed Up!</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: justified; color: white;'>Fed Up! provides you with personalized meal recommendations based on your food preferences and personal diet plan.</h3>", unsafe_allow_html=True)

    menu = ["","Log in","Sign up"]
    choice = st.selectbox("Log in or sign up",menu)

    if choice == "":
        st.markdown("<h2 style='text-align: justified; font-weight: bold; color: black;'></h2>", unsafe_allow_html=True)


    # Log in to your account
    elif choice == "Log in":
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


if __name__ == '__main__':
    main()
