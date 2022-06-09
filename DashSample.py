# Import required libraries
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, no_update
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

tab = 'tab-1'
root = Path('input', 'iris')
file = 'iris.csv'
df_data = pd.read_csv(root / file)

# Create a dash application
app = Dash(__name__)

#Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.Div([
        html.Div(id='dummy'),
        html.H1('Iris Data Visualization'),
        dcc.Tabs(id="tabs-example-graph", value='tab-1', children=[
            dcc.Tab(label='Settings', value='tab-1', children=[
                    html.H3('Select x axis'),
                    dcc.RadioItems(
                            id='select-x', 
                            options= ['petal_width', 'petal_length', 'sepal_width', 'sepal_length'],
                            value='petal_width',
                            inline=True
                    ),
                    html.H3('Select y axis'),
                    dcc.RadioItems(
                            id='select-y',
                            options= ['petal_width', 'petal_length', 'sepal_width', 'sepal_length'],
                            value='petal_length',
                            inline=True
                    ),
                    html.H3('Select size'),
                    dcc.Slider(id='select-size', min=1, max=9, marks={i: f'Size {i}' for i in range(10)})
                ]),
            dcc.Tab(label='Graph', value='tab-2', children=[
                    html.Div(id='graph-output-wrapper'),
                ]),
        ]),
        html.Div(id='tabs-content-example-graph')
    ], style={'display':'block'})
])

@app.callback(
    Output('graph-output-wrapper', 'children'),
    Input('select-x', 'value'),
    Input('select-y', 'value'))
def render_content(x, y):
    if x == y:
        return html.Div([
            html.H3('Error: x and y axis must be different values'),
        ])
    return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs-dcc',
                figure=px.scatter(df_data, x=x, y=y, color='species',title=x+' vs '+y)
            )
        ])

app.clientside_callback(
    """
    function(tab_value) {
        if (tab_value === 'tab-1') {
            document.title = 'Settings';
        } else if (tab_value === 'tab-2') {
            document.title = 'Dashboard';
        }
        return null;
    }
    """,
    Output('dummy', 'children'),
    Input('tabs-example-graph', 'value')
)

if __name__ == '__main__':
    app.run_server(debug=True, port=3000)