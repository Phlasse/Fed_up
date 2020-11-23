"""Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st
import welcome
import recommendations
import foodinder


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
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
    app.add_app("Main", welcome.main)
    app.add_app("Foodinder", foodinder.main)
    app.add_app("Recommendations", recommendations.main)
    app.run()
