import pandas as pd
import numpy as np
import altair as alt
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px

df = pd.read_csv('../data/clean_data.csv')

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css', '/style.css'])
server = app.server

app.layout = html.Div([

        html.H1("Who Are in the Olympics?",
                style = {'color': 'white', 'text-align': 'left', 'padding': '0px 0px 0px 20px', 'margin-bottom': '-10px'}),
        html.H4("Insights for Olympic Athlete Information since 1896", 
                style = {'color': 'white', 'text-align': 'left', 'border-bottom': '1px solid black', 'padding': '0px 0px 10px 20px'}),
        
        # Main Container Div
        html.Div([

            # Sidebar (Filter) Div
            html.Div([
                html.H2("Filters", style = {'flex-grow': '1', 
                                            'margin': '0px',
                                            'border-bottom': '2px solid white', 
                                            'line-height': '1'}),
                html.Div([
                    html.H5("Drag Slider To Select Years"),
                    dcc.RangeSlider(
                        min = 1896, max = 2016,
                        marks = {i: {'label': f'{i+4}', 'style': {'transform': 'rotate(90deg)', 'color': 'white'}} for i in range(1896, 2016, 8)},
                        id = 'year_range',
                        value = [1896, 2016],
                        tooltip={"placement": "top", "always_visible": True}
                    )
                ], style = {'width': '100%', 'flex-grow': '2'}),
                html.Div([
                    html.H5("Select Sports"),
                    dcc.Dropdown(
                        options=['All'] + np.sort(df.Sport.unique()).tolist(),
                        value=['All'],
                        multi=True,
                        id='sport'
                    )
                ], style = {'width': '100%', 'color': 'black', 'flex-grow': '1.5'}),
                html.Div([
                    html.H5("Select Countries"),
                    dcc.Dropdown(
                        options=['All'] + np.sort(df.Team.unique()).tolist(),
                        value=['All'],
                        multi=True,         
                        id='country'
                    )
                ], style = {'width': '100%', 'color': 'black', 'flex-grow': '1.5'}),
                html.Div([
                    html.H5("Medal Filter"),
                    dcc.RadioItems(
                        options=['Gold', 'Silver', 'Bronze'] + ['All'],
                        value='All',
                        id='medals',
                        inline=True
                    )
                ], style = {'width': '100%', 'flex-grow': '1', 'color': 'white'}),
                html.Div([
                    html.H5("Season Filter"),
                    dcc.RadioItems(
                        options=df.Season.unique().tolist() + ['Both'],
                        value='Both',
                        id='season',
                        inline=True
                    )
                ], style = {'width': '100%', 'flex-grow': '4', 'color': 'white'})
            ], style = {'width': '23%', 'margin-top': '0px', 'padding': '25px', 
                    'background-color': '#544F78', 'border-radius': '10px',
                    'display': 'flex', 'justify-content': 'space-around', 'flex-direction': 'column'}),

            # Graph Container Div         
            html.Div([
                dcc.Tabs([
                    dcc.Tab(label='Plots', children=[
                        dcc.Loading(
                            id = 'loading',
                            children = [
                                dcc.Graph(id='hist', 
                                        style = {'height': '350px', 'width': '33%', 'display': 'inline-block'},
                                        config={
                                            'displayModeBar':False
                                }),
                                dcc.Graph(id='hist2', 
                                        style = {'height': '350px', 'width': '33%', 'display': 'inline-block'},
                                        config={
                                            'displayModeBar':False
                                }),
                                dcc.Graph(id='hist3', 
                                        style = {'height': '350px', 'width': '33%', 'display': 'inline-block'},
                                        config={
                                            'displayModeBar':False
                                }),
                                dcc.Graph(id='map', 
                                            style = {'height': '500px', 'width': '99%'},
                                            config={
                                                'displayModeBar':False
                                })
                            ], type = 'cube'
                        )
                        ],
                            className='custom-tab',
                            selected_className='custom-tab--selected'),
                    dcc.Tab(label='Data Table', children = [
                        html.Br(),
                        dash_table.DataTable(data=df.sample(100).to_dict('records'), 
                                    columns=[{"name": i, "id": i} for i in df.columns], 
                                    id = 'tbl', 
                                    style_cell = {'color': 'black', 'whiteSpace': 'normal'}, 
                                    style_header = {'color': 'white', 'backgroundColor': '#322c4a', 'border': '0px solid white', 'fontWeight': 'bold', 'textAlign': 'left'},
                                    style_data = {'backgroundColor': '#96293F'},
                                    style_data_conditional = [
                                        {
                                            'if': {'column_id': ['ID', 'Sex', 'Height', 'Team', 'Games', 'Season', 'Sport', 'Medal']},
                                            'backgroundColor': '#B33951'
                                        }
                                    ],
                                    page_action='native', 
                                    page_size=20)
                    
                        ],
                            className='custom-tab',
                            selected_className='custom-tab--selected')
                ])
                ], style = {'width': '70%', 'overflow': 'hidden', 'height': '950px', 
                            'background-color': '#544F78', 'border-radius': '10px', 
                            'padding': '1%'})
            ], style = {'display': 'flex', 'justify-content': 'space-around'})
        ], style = {'display': 'fixed', 'height': '100%', 'background-color': '#322c4a'})

def filter_data(data, year_range=(1896, 2016), season='Both', medals='All', sport=['All'], country=['All']):

    year_filter = (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
    season_filter = True if season == 'Both' else (df['Season'] == season)
    medal_filter = True if medals == 'All' else (df['Medal'] == medals)
    sport_filter = True if 'All' in sport else (df['Sport'].isin(sport))
    country_filter = True if 'All' in country else (df['Team'].isin(country))
    
    data = data[year_filter & season_filter & sport_filter & country_filter & medal_filter]

    return data

@app.callback(
    Output('tbl', 'data'),
    Input('year_range', 'value'),
    Input('sport', 'value'),
    Input('country', 'value'),
    Input('medals', 'value'),
    Input('season', 'value')
)
def update_table(year_range, sport, country, medals, season):
    filtered = filter_data(df, year_range=year_range, sport=sport, country=country, medals=medals, season=season)
    return filtered.sample(80).to_dict('records')


styling_template = {'title': {'font': {'size': 21, 'family': 'helvetica', 'color': 'white'}, 'x': 0,
                        'xref':'paper', 'y': 1, 'yanchor': 'bottom', 'yref':'paper', 'pad':{'b': 10}},
                'legend': {'font': {'color': 'white'}},
             'margin': dict(l=20, r=20, t=50, b=20),
             'paper_bgcolor': 'rgba(0,0,0,0)', 
             'plot_bgcolor': 'rgba(0,0,0,0)', 
             'colorway': ['black'],
             'xaxis': {
                 'color': 'white'
             },
             'yaxis': {
                 'color': 'white'
             }}

map_styles = {
    'title': {'x': 0.1, 'pad':{'b': 10}},
    'geo': {'bgcolor': 'rgba(0,0,0,0)',
            'framecolor': 'rgba(0,0,0,0)', 
            'landcolor': '#fcf7e1', 
            'lakecolor': '#97c7f7'},
    'coloraxis': {
        'colorbar': {'title': {'font': {'color': 'white', 'family': 'helvetica'}},
                    'tickfont': {'color': 'white', 'family': 'helvetica'}},
        'colorscale': 'reds'
    }
}

# Function which takes filtered data and plots the two histograms
@app.callback(
    Output('hist', 'figure'),
    Output('hist2', 'figure'),
    Output('hist3', 'figure'),
    Input('year_range', 'value'),
    Input('sport', 'value'),
    Input('country', 'value'),
    Input('medals', 'value'),
    Input('season', 'value')
)
def update_graphs(year_range, sport, country, medals, season):
    filtered = filter_data(df, year_range=year_range, sport=sport, country=country, medals=medals, season=season)
    fig = px.histogram(data_frame=filtered, nbins=50, x='Height', color='Sex', opacity=0.8, barmode='overlay', title='Distribution of Athlete Heights')
    fig.update_layout(styling_template)
    fig.update_layout({'xaxis': {'range': [110, 225], 'title': {'text': 'Height (cm)'}}})

    fig2 = px.histogram(data_frame=filtered, x='Age', color='Sex', opacity=0.8, barmode='overlay', title='Distribution of Athlete Ages')
    fig2.update_layout(styling_template)
    fig2.update_layout({'xaxis': {'range': [10, 60], 'title': {'text': 'Age (years)'}}})

    fig3 = px.histogram(data_frame=filtered, nbins=50, x='Weight', color='Sex', opacity=0.8, barmode='overlay', title='Distribution of Athlete Weights')
    fig3.update_layout(styling_template)
    fig3.update_layout({'xaxis': {'range': [30, 200], 'title': {'text': 'Weight (kgs)'}}})

    return fig, fig3, fig2

# Function which takes filtered data, does additional aggregation, and plots the choropleth
@app.callback(
    Output('map', 'figure'),
    Input('year_range', 'value'),
    Input('sport', 'value'),
    Input('country', 'value'),
    Input('medals', 'value'),
    Input('season', 'value')
)
def update_map(year_range, sport, country, medals, season):
    filtered = filter_data(df, year_range=year_range, sport=sport, country=country, medals=medals, season=season)
    grouped = filtered.groupby('Team')['Name'].nunique().to_frame().reset_index()
    grouped.rename(columns = {'Team': 'Country', 'Name': 'Number of Athletes'}, inplace = True)
    map = px.choropleth(grouped,
              locations = 'Country',
              locationmode = 'country names',
              color = 'Number of Athletes',
              title='Number of Athletes Per Country')
    map.update_layout(styling_template)
    map.update_layout(map_styles)
    
    return map

if __name__ == '__main__':
    app.run_server(debug=True)