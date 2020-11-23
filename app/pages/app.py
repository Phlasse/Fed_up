"""Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st

import preferences
import roulette
import recommendation
import checkout
import dashboard


CSS = """
"""

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

# img_fed_up = Image.open("Fed_up/data/samples/logo.png")
# img_fed_up_sidebar = Image.open("Fed_up/data/samples/sidebar_logo.png")
# st.sidebar.image(img_fed_up_sidebar, width=200)


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):

        app = st.sidebar.radio(
            ' ',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()


if __name__ == "__main__":

    app = MultiApp()
    app.add_app("Profile", preferences.run)
    app.add_app("Food Roulette", roulette.run)
    app.add_app("Recommendations", recommendation.run)
    app.add_app("Checkout", checkout.run)
    app.add_app("Dashboard", dashboard.run)
    app.run()
