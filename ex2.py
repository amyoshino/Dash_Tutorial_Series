## Bootstrap Grid tutorial - adding style to the app

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

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
                        'height': '15%',
                        'width': '15%',
                        'float': 'right',
                        'position': 'relative',
                        'margin-top': 10,
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
            html.Div([
                dcc.Graph(
                    id='example-graph',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                        ],
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
                )
                ], className= 'six columns'
                ),

                html.Div([
                dcc.Graph(
                    id='example-graph-2',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 9, 8], 'type': 'line', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'Graph 2'
                        }
                    }
                )
                ], className= 'six columns'
                )
            ], className="row"
        )
    ], className='ten columns offset-by-one')
)

if __name__ == '__main__':
    app.run_server(debug=True)
