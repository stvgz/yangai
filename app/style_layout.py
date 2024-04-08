# from app.style import style_no_padding
# 8/30 make a function to build content from navbar+sidebar+main content
import dash
import dash.dependencies as dd
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import dash_bootstrap_components as dbc

from style import *
from navbar import navbar

def make_app_page(app,navbar=navbar,content_side=[],content_main=[],content_main_style=content_style):
    app.layout=html.Div(
            style=content_style,
            children=[
            # dcc.Location(id="url"),
            dbc.Row(
                [
                    dbc.Col(navbar)
                ]
            ),
            dbc.Row(
                [
                    # dbc.Col(sidebar,width=2),
                    dbc.Col(content_main)
                ]
            )
        ])

    return app