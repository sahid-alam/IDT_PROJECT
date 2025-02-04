import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Read your CSV data
data = pd.read_csv('data.csv')

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Get unique countries and years from data
countries = data['Country Name'].unique()
years = data['Year'].unique()

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Global Carbon Emissions Dashboard", 
                        className="text-center mb-4"),
                width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='country-selector',
                options=[{'label': 'All Countries', 'value': 'All'}] + 
                        [{'label': c, 'value': c} for c in countries],
                value='All',
                className='mb-3'
            )
        ], md=6),
        dbc.Col([
            dcc.Dropdown(
                id='year-selector',
                options=[{'label': y, 'value': y} for y in years],
                value=2022,
                className='mb-3'
            )
        ], md=6)
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-chart'), md=6),
        dbc.Col(dcc.Graph(id='pie-chart'), md=6)
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='line-chart'), md=12)
    ])
], fluid=True)

# Callbacks for interactivity
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('line-chart', 'figure')],
    [Input('country-selector', 'value'),
     Input('year-selector', 'value')]
)
def update_graphs(selected_country, selected_year):
    # Bar Chart Logic
    if selected_country == 'All':
        bar_data = data[data['Year'] == selected_year]
        x_axis = 'Country Name'
        title_suffix = f'({selected_year})'
    else:
        bar_data = data[data['Country Name'] == selected_country]
        x_axis = 'Year'
        title_suffix = f'for {selected_country}'
    
    bar_fig = px.bar(
        bar_data,
        x=x_axis,
        y='CO2 Emissions (million tons)',
        title=f'Emissions Distribution {title_suffix}',
        color=x_axis,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hover_data=['Notes']
    )
    
    # Pie Chart - Updated to show all countries for selected year
    pie_fig = px.pie(
        data[data['Year'] == selected_year],
        names='Country Name', 
        values='CO2 Emissions (million tons)',
        title=f'Global Emissions Distribution ({selected_year})',
        hole=0.4,
        hover_data=['Notes']
    )
    
    # Line Chart
    line_fig = px.line(
        data, x='Year', y='CO2 Emissions (million tons)', 
        color='Country Name',
        title='Emission Trends Over Time',
        markers=True,
        hover_data=['Notes']
    )
    
    # Update layout for all figures
    for fig in [bar_fig, pie_fig, line_fig]:
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            margin=dict(t=40, b=20),
            height=400
        )
        
    return bar_fig, pie_fig, line_fig

if __name__ == '__main__':
    app.run_server(debug=True) 