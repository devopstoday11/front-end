import os
import pathlib
import re

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State

# stylesheet tbd
# external_stylesheets = [
#     dbc.themes.BOOTSTRAP, # Bootswatch theme
#     'https://use.fontawesome.com/releases/v5.9.0/css/all.css', # for social media icons
# ]

# Initialize app
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
# app.config.supress_callback_exceptions = True
app.title = 'COVID19 US Dashboard' # for browser titlebar
server = app.server
# # Load data

# APP_PATH = str(pathlib.Path(__file__).parent.resolve())

# df_lat_lon = pd.read_csv(
#     os.path.join(APP_PATH, os.path.join("data", "lat_lon_counties.csv"))
# )

