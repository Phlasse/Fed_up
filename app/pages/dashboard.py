import pandas as pd
import numpy as np

import streamlit as st
import streamlit.components.v1 as components

import base64
from PIL import Image
from io import BytesIO
import requests
import ipdb
import time
import os


def run():
    # Display headers
    st.write("# Dashboard")
    st.write(f"📊 Check your nutrition stats.")
    st.markdown("---")
