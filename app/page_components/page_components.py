import dash_bootstrap_components as dbc

example_form={
    
        'label':'x',
        'x':'x'
    
}


# text input
input_text_01=dbc.FormGroup(
    [
        # dbc.Label("Input Serial Number", html_for="example-email"),
        dbc.Label("Input Serial Number"),
        dbc.Input(type="email", id="input_text_01", placeholder="TG320xx"),
        dbc.FormText(
            "Input serial, seperate with , if multiple",
            color="secondary",
        ),
    ]
)


def create_component_input_text(label,id_input,placeholder='Placeholder',form_text=''):
    """
    create  a input group with label and text
    """
    comp=dbc.FormGroup(
        [
            # dbc.Label("Input Serial Number", html_for="example-email"),
            dbc.Label(label),
            dbc.Input(placeholder=placeholder,id=id_input),
            dbc.FormText(form_text
            ),
        ]
    )
    return comp

# dropdown
import dash_core_components as dcc



dcc.Dropdown(
    options=[
        {'label': 'New York City', 'value': 'NYC'},
        {'label': 'Montréal', 'value': 'MTL'},
        {'label': 'San Francisco', 'value': 'SF'}
    ],
    value='MTL'
)  

import dash_core_components as dcc

dcc.Dropdown(
    options=[
        {'label': 'New York City', 'value': 'NYC'},
        {'label': 'Montréal', 'value': 'MTL'},
        {'label': 'San Francisco', 'value': 'SF'}
    ],
    multi=True,
    value="MTL"
)  
import dash_bootstrap_components as dbc
import dash_core_components as dcc

example_form={
    
        'label':'x',
        'x':'x'
    
}



#intervals for callback, this list will be added into content of very page
interval_list_all=[
    dcc.Interval(
        id='interval_3m',
        # interval=60 * 60 * 1000,  # in milliseconds
        interval=60 * 60 * 1000,  # in milliseconds
        n_intervals=0),
    dcc.Interval(
        id='interval_5m',
        # interval=60 * 60 * 1000,  # in milliseconds
        interval=60 * 60 * 1000,  # in milliseconds
        n_intervals=0),
    dcc.Interval(
        id='interval_10m',
        # interval=60 * 60 * 1000,  # in milliseconds
        interval=60 * 60 * 1000,  # in milliseconds
        n_intervals=0),
    dcc.Interval(
        id='interval_30m',
        # interval=60 * 60 * 1000,  # in milliseconds
        interval=60 * 60 * 1000,  # in milliseconds
        n_intervals=0),
    dcc.Interval(
        id='interval_60m',
        # interval=60 * 60 * 1000,  # in milliseconds
        interval=60 * 60 * 1000,  # in milliseconds
        n_intervals=0),
    dcc.Interval(
        id='interval_3h',
        # interval=60 * 60 * 1000,  # in milliseconds
        interval=60 * 60 * 1000,  # in milliseconds
        n_intervals=0),
    dcc.Interval(
        id='interval_6h',
        # interval=60 * 60 * 1000,  # in milliseconds
        interval=60 * 60 * 1000,  # in milliseconds
        n_intervals=0),
    dcc.Interval(
        id='interval_12h',
        # interval=60 * 60 * 1000,  # in milliseconds
        interval=60 * 60 * 1000,  # in milliseconds
        n_intervals=0)]


# text input
input_text_01=dbc.FormGroup(
    [
        # dbc.Label("Input Serial Number", html_for="example-email"),
        dbc.Label("Input Serial Number"),
        dbc.Input(type="email", id="input_text_01", placeholder="TG320xx"),
        dbc.FormText(
            "Input serial, seperate with , if multiple",
            color="secondary",
        ),
    ]
)


def create_component_input_text(label,id_input,placeholder='Placeholder',form_text=''):
    """
    create  a input group with label and text
    """
    comp=dbc.FormGroup(
        [
            # dbc.Label("Input Serial Number", html_for="example-email"),
            dbc.Label(label),
            dbc.Input(placeholder=placeholder,id=id_input),
            dbc.FormText(form_text
            ),
        ]
    )
    return comp
