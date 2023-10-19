#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import json

app = dash.Dash(__name__)  
server = app.server
app.title = "Fire Dashboard"

# Reading the dataset
df = pd.read_csv("altered_df.csv")

# Your GeoJSON data
with open('geo.txt', 'r') as f:
    geojson_data = json.load(f)

# Function which will render bar graph for area burned
def get_area_burned(year):
    global df
    year_df = df[df["Year"] == year].copy()

    fig = px.bar(
        year_df,
        x="FireName",
        y="AreaHa",
        color="AreaHa",
        labels={"FireName": "Fire Name", "AreaHa": "Area Burned (Hectares)"},
        height=400,
        width=500,
        title=f"Area Burned in {year}",
        template="plotly_dark",
    )
    fig.update_layout({"paper_bgcolor": "#282828", "plot_bgcolor": "#282828"})
    return fig

# Function which will render bar graph for total fires per year
def get_total_fires():
    global df
    total_fires_df = df.groupby("Year").size().reset_index(name="Total Fires")

    fig = px.bar(
        total_fires_df,
        x="Year",
        y="Total Fires",
        labels={"Year": "Year", "Total Fires": "Total Fires"},
        height=400,
        width=500,
        title="Total Fires per Year",
        template="plotly_dark",
    )
    fig.update_layout({"paper_bgcolor": "#282828", "plot_bgcolor": "#282828"})
    return fig

# Function to get linear regression predictions
def get_linear_regression_predictions():
    X = df[['Year']]
    y = df['target']
    
    model = LinearRegression()
    model.fit(X, y)
    
    future_years = list(range(df['Year'].min(), 2051))
    future_predictions = model.predict([[year] for year in future_years])
    
    # Create a scatter plot for existing data points and a line plot for predictions
    fig = go.Figure()
    
    # Scatter plot for existing data points
    fig.add_trace(go.Scatter(
        x=df['Year'],
        y=y,
        mode='markers',
        name='Actual Total Fires',
        marker=dict(color='black')
    ))
    
    # Line plot for linear regression predictions
    fig.add_trace(go.Scatter(
        x=future_years,
        y=future_predictions,
        mode='lines',
        name='Predicted Total Fires',
        line=dict(color='blue', width=3)
    ))
    
    layout = go.Layout(
        title='Linear Regression Model',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Total Fires'),
        legend=dict(x=0, y=1),
        template="plotly_dark",
    )
    
    fig.update_layout(layout)
    
    return fig

# Creating CSS for the main div
main_div_style = {
    "background-color": "#181818",
    "padding": "10px",
    "width": "100%",
    "height": "100vh",  # Set a fixed height
    "overflowY": "auto",  # Enable vertical scrolling if needed
}

# Creating options for dropdown display
options = [{"label": year, "value": year} for year in df["Year"].unique()]

# Creating dropdown section
dropdown_box = html.Div(
    children=[
        dcc.Dropdown(
            id="year_selector",
            options=options,
            clearable=False,
            value=df["Year"].min(),
            placeholder="Select a year",
        )
    ],
    style={
        "width": "90%",
        "position": "fixed",
        "left": "5%",
        "display": "inline-block",
        "top": "1%",
        "z-index": "1",
    },
)

# Creating graphs section
Graphs = html.Div(
    children=[
        html.Div(
            children=[dcc.Graph(id="areaBurned")],
            style={
                "width": "45%",
                "position": "relative",  # Allow relative positioning
                "margin": "auto",  # Center the graph
                "background-color": "#282828",
                "top": "10%",
            },
        ),
        html.Div(
            children=[dcc.Graph(id="totalFires")],
            style={
                "width": "45%",
                "position": "relative",  # Allow relative positioning
                "margin": "auto",  # Center the graph
                "background-color": "#282828",
                "top": "10%",
            },
        ),
        html.Div(
            children=[dcc.Graph(id="linearRegression")],
            style={
                "width": "90%",
                "position": "relative",  # Allow relative positioning
                "margin": "auto",  # Center the graph
                "background-color": "#282828",
                "top": "60%",
            },
        ),
        html.Div(
            children=[dcc.Graph(id="fire-map")],
            style={
                "width": "90%",
                "position": "relative",  # Allow relative positioning
                "margin": "auto",  # Center the graph
                "background-color": "#282828",
                "top": "75%",
            },
        ),
    ]
)


# Creating the main layout
app.layout = html.Div(
    id="main_div", children=[
        dcc.Loading(
            children=[
                html.Div(
                    children=[dropdown_box, Graphs],
                    style={
                        "width": "90%",
                        "position": "relative",
                        "margin": "auto",
                    },
                ),
            ],
            type="default",
        ),
    ],
    style=main_div_style
)

@app.callback(
    Output(component_id="areaBurned", component_property="figure"),
    [Input(component_id="year_selector", component_property="value")],
)
def update_area_burned(year):
    fig = get_area_burned(year)
    return fig

@app.callback(
    Output(component_id="totalFires", component_property="figure"),
    [Input(component_id="year_selector", component_property="value")],
)
def update_total_fires(year):
    fig = get_total_fires()
    return fig

@app.callback(
    Output(component_id="linearRegression", component_property="figure"),
    [Input(component_id="year_selector", component_property="value")],
)
def update_linear_regression_predictions(year):
    fig = get_linear_regression_predictions()
    return fig


# Callback to update the map based on user input
@app.callback(
    Output('fire-map', 'figure'),
    [Input('year_selector', 'value'),
     Input('fire-map', 'clickData')]  # Add clickData as an input
)
def update_map(selected_year, click_data):
    # Create a color scale where areas are blue by default
    color_scale = px.colors.sequential.Blues

    if selected_year is not None:
        # If a specific year is selected, set a different color for highlighting
        highlighted_color = 'orange'  # Choose the color you want for highlighting
        color_scale = [highlighted_color if name in df[df['Year'] == selected_year]['FireName'].values else 'blue' for name in df['FireName']]

    fig = px.choropleth_mapbox(
        geojson=geojson_data,
        featureidkey="properties.FireName",
        locations=df['FireName'],
        color=df['AreaHa'],
        color_continuous_scale=color_scale,
        center={"lat": -30, "lon": 152},
        mapbox_style="open-street-map",
        opacity=0.5,
        title=f"Fire Areas in {selected_year}" if selected_year else "All Fire Areas",
    )

    if click_data:  # Check if there is click data
            clicked_area = click_data['points'][0]['location']
            # Update the color of the clicked area
            area_value = df[df['FireName'] == clicked_area]['AreaHa'].values[0]
            fig.update_geos(color=area_value)

            # Define hovertemplate to display FireName, AreaHa, and Year
    hover_template = "<b>%{properties.FireName}</b><br>Area: %{z}<br>Year: %{customdata}"
    fig.update_traces(hovertemplate=hover_template, customdata=df['Year'])

            # Update the layout of the map
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        geo=dict(
            center={"lat": -30, "lon": 152},
            projection_scale=8,
            visible=False
        )
    )

    return fig


# Callback to update the selected year when an area is clicked
@app.callback(
    Output('year_selector', 'value'),
    [Input('fire-map', 'clickData')],
    [State('year_selector', 'value')]
)
def update_selected_year(click_data, current_year):
    if click_data:
        # Update the selected year based on the clicked area
        clicked_area = click_data['points'][0]['location']
        clicked_year = df[df['FireName'] == clicked_area]['Year'].values[0]
        return clicked_year
    else:
        return current_year


if __name__ == "__main__":
    app.run_server(debug=False, port=8080)

