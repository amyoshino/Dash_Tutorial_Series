## Evolving from the basics

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd

from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output, State, Event

app = dash.Dash(__name__)
server = app.server
app.title = 'NYC Wi-Fi Hotspots'

# API keys and datasets
mapbox_access_token = 'USE YOUR MAPBOX KEY HERE'
map_data = pd.read_csv("nyc-wi-fi-hotspot-locations.csv")

# Selecting only required columns
map_data = map_data[["Borough", "Type", "Provider", "Name", "Location", "Latitude", "Longitude"]].drop_duplicates()

# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

#  Layouts
layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
)
layout_table['font-size'] = '12'
layout_table['margin-top'] = '20'

layout_map = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='WiFi Hotspots in NYC',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-73.91251,
            lat=40.7342
        ),
        zoom=10,
    )
)

# functions
def gen_map(map_data):
    # groupby returns a dictionary mapping the values of the first field
    # 'classification' onto a list of record dictionaries with that
    # classification value.
    return {
        "data": [{
                "type": "scattermapbox",
                "lat": list(map_data['Latitude']),
                "lon": list(map_data['Longitude']),
                "hoverinfo": "text",
                "hovertext": [["Name: {} <br>Type: {} <br>Provider: {}".format(i,j,k)]
                                for i,j,k in zip(map_data['Name'], map_data['Type'],map_data['Provider'])],
                "mode": "markers",
                "name": list(map_data['Name']),
                "marker": {
                    "size": 6,
                    "opacity": 0.7
                }
        }],
        "layout": layout_map
    }

app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(children='Maps and Tables',
                        className='nine columns'),
                html.Img(
                    src="https://www.fulcrumanalytics.com/wp-content/uploads/2017/12/cropped-site-logo-1.png",
                    className='three columns',
                    style={
                        'height': '16%',
                        'width': '16%',
                        'float': 'right',
                        'position': 'relative',
                        'padding-top': 12,
                        'padding-right': 0
                    },
                ),
                html.Div(children='''
                        Dash Tutorial video 04: Working with tables and maps.
                        ''',
                        className='nine columns'
                )
            ], className="row"
        ),

        # Selectors
        html.Div(
            [
                html.Div(
                    [
                        html.P('Choose Borroughs:'),
                        dcc.Checklist(
                                id = 'boroughs',
                                options=[
                                    {'label': 'Manhattan', 'value': 'MN'},
                                    {'label': 'Bronx', 'value': 'BX'},
                                    {'label': 'Queens', 'value': 'QU'},
                                    {'label': 'Brooklyn', 'value': 'BK'},
                                    {'label': 'Staten Island', 'value': 'SI'}
                                ],
                                values=['MN', 'BX', "QU",  'BK', 'SI'],
                                labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.P('Type:'),
                        dcc.Dropdown(
                            id='type',
                            options= [{'label': str(item),
                                                  'value': str(item)}
                                                 for item in set(map_data['Type'])],
                            multi=True,
                            value=list(set(map_data['Type']))
                        )
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                )
            ],
            className='row'
        ),

        # Map + table + Histogram
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='map-graph',
                                  animate=True,
                                  style={'margin-top': '20'})
                    ], className = "six columns"
                ),
                html.Div(
                    [
                        dt.DataTable(
                            rows=map_data.to_dict('records'),
                            columns=map_data.columns,
                            row_selectable=True,
                            filterable=True,
                            sortable=True,
                            selected_row_indices=[],
                            id='datatable'),
                    ],
                    style = layout_table,
                    className="six columns"
                ),
                html.Div([
                        dcc.Graph(
                            id='bar-graph'
                        )
                    ], className= 'twelve columns'
                    ),
                html.Div(
                    [
                        html.P('Developed by Adriano M. Yoshino - ', style = {'display': 'inline'}),
                        html.A('amyoshino@nyu.edu', href = 'mailto:amyoshino@nyu.edu')
                    ], className = "twelve columns",
                       style = {'fontSize': 18, 'padding-top': 20}
                )
            ], className="row"
        )
    ], className='ten columns offset-by-one'))

@app.callback(
    Output('map-graph', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
def map_selection(rows, selected_row_indices):
    aux = pd.DataFrame(rows)
    temp_df = aux.ix[selected_row_indices, :]
    if len(selected_row_indices) == 0:
        return gen_map(aux)
    return gen_map(temp_df)

@app.callback(
    Output('datatable', 'rows'),
    [Input('type', 'value'),
     Input('boroughs', 'values')])
def update_selected_row_indices(type, borough):
    map_aux = map_data.copy()

    # Type filter
    map_aux = map_aux[map_aux['Type'].isin(type)]
    # Boroughs filter
    map_aux = map_aux[map_aux["Borough"].isin(borough)]

    rows = map_aux.to_dict('records')
    return rows

@app.callback(
    Output('bar-graph', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)

    layout = go.Layout(
        bargap=0.05,
        bargroupgap=0,
        barmode='group',
        showlegend=False,
        dragmode="select",
        xaxis=dict(
            showgrid=False,
            nticks=50,
            fixedrange=False
        ),
        yaxis=dict(
            showticklabels=True,
            showgrid=False,
            fixedrange=False,
            rangemode='nonnegative',
            zeroline='hidden'
        )
    )

    data = Data([
         go.Bar(
             x=dff.groupby('Borough', as_index = False).count()['Borough'],
             y=dff.groupby('Borough', as_index = False).count()['Type']
         )
     ])

    return go.Figure(data=data, layout=layout)

if __name__ == '__main__':
    app.run_server(debug=True)
