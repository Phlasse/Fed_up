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
            'Go To',
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
