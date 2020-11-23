"""Frameworks for running multiple Streamlit applications as a single app.
"""

import pandas as pd
import streamlit as st

import welcome
import recommendation

@st.cache
def load_result():
    data = pd.read_csv("../Fed_up/data/preprocessed/data_preprocessed_recipe_pp_20201117_1347.csv")
    return data


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
        return 0

    def run(self, page='Main', arguments=''):

        for app in self.apps:
            if app['title'] == page:
                if arguments != '':
                    app['function'](arguments)

                else:
                    app['function']()
        #function()
        # app = st.sidebar.radio(
        #     'Go To',
        #     self.apps,
        #     format_func=lambda app: appRecommendation['title'])
        return 0


if __name__ == "__main__":

    app = MultiApp()
    app.add_app("Main", welcome.main)
    #app.add_app("Recommendation", recommendation.reco)
    app.run()
