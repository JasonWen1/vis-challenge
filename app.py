# coding:utf-8
from flask import Flask
from flask import send_file
import os

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash

import level1_data as dt1
import level3_data as dt3
import level2


server = Flask(__name__)
app = dash.Dash(__name__, server=server)
home = os.path.abspath(__file__)

app.layout = html.Div([
    # level
    html.H1(children='Level 1'),
    dcc.Dropdown(
        id='level1_temp_options',
        options=[
            {'label': 'Max Temperature', 'value': 'max'},
            {'label': 'Min Temperature', 'value': 'min'},
        ],
        value='max'
    ),
    dcc.Graph(id='level1-graph'),

    # level2
    html.A(href='/level2', children=[
        html.H1(children='Level 2')
    ]),

    # level3
    html.H1(children='Level 3'),
    dcc.Graph(id='level3-graph-1', figure=dt3.fig_node_link),
    dcc.Graph(id='level3-graph-2', figure=dt3.fig_matrix)

], style={'width': '18%', 'display': 'inline-block'})


@app.callback(Output('level1-graph', 'figure'), [Input('level1_temp_options', 'value')])
def level1_update_graph(selected_temp_option):
    return dt1.level1_update_graph(selected_temp_option)


@app.callback(Output('level3-graph-2', 'figure'), [Input('level3-graph-1', 'hoverData')])
def call_matrix(hoverData):
    fig = dt3.update_matrix(hoverData)
    if fig:
        return fig
    else:
        return dt3.fig_matrix


@app.callback(Output('level3-graph-1', 'figure'), [Input('level3-graph-2', 'hoverData')])
def call_node_link(hoverData):
    fig = dt3.update_node(hoverData)
    if fig:
        return fig
    else:
        return dt3.fig_node_link


@server.route('/level2')
def level2():
    return send_file('level2.svg')


if __name__ == '__main__':
    app.run_server()
