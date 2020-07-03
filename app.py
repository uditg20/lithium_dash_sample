#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 19:44:52 2020

@author: uditgupta
"""


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import flask
import pandas as pd
import time
import os

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/hello-world-stock.csv')
df = pd.read_csv('https://raw.githubusercontent.com/uditg20/lithium_dash_sample/master/data.csv')


app = dash.Dash('app', server=server)

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.H1('Metric Tonnes of Lithium'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Exports', 'value': 'Exports'},
            {'label': 'Imports', 'value': 'Imports'},
            {'label': 'Consumption', 'value': 'Consumption'}
        ],
        value='Exports'
    ),
    dcc.Graph(id='my-graph')
], className="container")

@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    dff = df[df['category'] == selected_dropdown_value]
    return {
        'data': [{
            'x': dff.year,
            'y': dff.value,
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }],
        'layout': {
            'margin': {
                'l': 30,
                'r': 20,
                'b': 30,
                't': 20
            }
        }
    }

if __name__ == '__main__':
    app.run_server()