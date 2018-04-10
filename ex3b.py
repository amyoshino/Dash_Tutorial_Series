## Evolving from the basics

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

all_options = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': [u'Montreal', 'Toronto', 'Ottawa'],
    'All': ['New York City', 'San Francisco', 'Cincinnati', u'Montreal', 'Toronto', 'Ottawa']
}

city_data = {
    'San Francisco': {'x': [1, 2, 3], 'y': [4, 1, 2]},
    'Montreal': {'x': [1, 2, 3], 'y': [2, 4, 5]},
    'New York City': {'x': [1, 2, 3], 'y': [2, 2, 7]},
    'Cincinnati': {'x': [1, 2, 3], 'y': [1, 0, 2]},
    'Toronto': {'x': [1, 2, 3], 'y': [4, 7, 3]},
    'Ottawa': {'x': [1, 2, 3], 'y': [2, 3, 3]}
}

# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})  # noqa: E501

app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(children='Hello World',
                        className='nine columns'),
                html.Img(
                    src="http://test.fulcrumanalytics.com/wp-content/uploads/2015/10/Fulcrum-logo_840X144.png",
                    className='three columns',
                    style={
                        'height': '9%',
                        'width': '9%',
                        'float': 'right',
                        'position': 'relative',
                        'padding-top': 0,
                        'padding-right': 0
                    },
                ),
                html.Div(children='''
                        Dash: A web application framework for Python.
                        ''',
                        className='nine columns'
                )
            ], className="row"
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.P('Choose City:'),
                        dcc.Checklist(
                                id = 'Cities',
                                options=[
                                    {'label': 'San Francisco', 'value': 'San Francisco'},
                                    {'label': 'Montreal', 'value': 'Montreal'}
                                ],
                                values=['San Francisco', 'Montreal'],
                                labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.P('Choose Country:'),
                        dcc.RadioItems(
                                id = 'Country',
                                options=[{'label': k, 'value': k} for k in all_options.keys()],
                                value='All',
                                labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                )
            ], className="row"
        ),

        html.Div(
            [
            html.Div([
                    dcc.Graph(
                        id='example-graph'
                    )
                ], className= 'six columns'
                ),

                html.Div([
                    dcc.Graph(
                        id='example-graph-2'
                    )
                ], className= 'six columns'
                )
            ], className="row"
        )
    ], className='ten columns offset-by-one')
)
@app.callback(
    dash.dependencies.Output('Cities', 'options'),
    [dash.dependencies.Input('Country', 'value')])
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]

@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('Cities', 'values')])
def update_image_src(selector):
    data = []
    for city in selector:
        data.append({'x': city_data[city]['x'], 'y': city_data[city]['y'],
                    'type': 'bar', 'name': city})
    figure = {
        'data': data,
        'layout': {
            'title': 'Graph 1',
            'xaxis' : dict(
                title='x Axis',
                titlefont=dict(
                family='Courier New, monospace',
                size=20,
                color='#7f7f7f'
            )),
            'yaxis' : dict(
                title='y Axis',
                titlefont=dict(
                family='Helvetica, monospace',
                size=20,
                color='#7f7f7f'
            ))
        }
    }
    return figure

@app.callback(
    dash.dependencies.Output('example-graph-2', 'figure'),
    [dash.dependencies.Input('Cities', 'values')])
def update_image_src(selector):
    data = []
    for city in selector:
        data.append({'x': city_data[city]['x'], 'y': city_data[city]['y'],
                    'type': 'line', 'name': city})
    figure = {
        'data': data,
        'layout': {
            'title': 'Graph 2',
            'xaxis' : dict(
                title='x Axis',
                titlefont=dict(
                family='Courier New, monospace',
                size=20,
                color='#7f7f7f'
            )),
            'yaxis' : dict(
                title='y Axis',
                titlefont=dict(
                family='Helvetica, monospace',
                size=20,
                color='#7f7f7f'
            ))
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
