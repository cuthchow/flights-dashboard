import altair as alt
from dash import Dash, dcc, html, Input, Output
from vega_datasets import data

flights = data.flights_10k()[:5000]

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div([
        html.H1("Flights Dashboard", 
            style = {'color': 'red', 'text-align': 'center'}
            ),
        html.Div([
            html.H5("Distance"),
            dcc.RangeSlider(
                min = 0, max = 1000,
                id = 'xrange',
                value = [0, 2000]
            ),
            html.H5("Origin"),
            dcc.Dropdown(
                options = list(flights['origin'].unique()),
                value = 'SJC',
                id = 'origin'
            )
        ], style = {'width': '50%'}),
        html.Iframe(
            id = 'scatter',
            style={'border-width': '0', 'width': '100%', 'height': '400px'})])

@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xrange', 'value'),
    Input('origin', 'value'))
def plot_altair(xrange, origin, df=flights.copy()):
    xmin, xmax = xrange
    chart = alt.Chart(df[(df['distance'] > xmin) & (df['distance'] < xmax) & (df['origin'] == origin)]).mark_point().encode(
        x='distance',
        y='delay')
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)