from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from coded_school.data import *
from urllib.request import urlopen
import json

app = Dash(__name__)

app.layout = html.Div([
    html.H4("Economic indicators for the city of Chicago by zip code"),
    html.P("Select data"),
    dcc.RadioItems(
        id="data",
        options=[
            {"label": "Poverty rate (%)", "value": "poverty_rate"},
            {"label": "Unemployment rate (%)", "value": "unemp_rate"},
            {"label": "High school enrollment rate (%)", "value": "hs_enrol_rate"},
            {"label": "Median income ($)", "value": "med_income"}
        ],
        value="med_income",  # Default value
        inline=True
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"),
    Input("data", "value"))
def display_choropleth(data):
    with urlopen("https://data.cityofchicago.org/api/geospatial/gdcf-axmw?method=export&format=GeoJSON") as response:
        zip_codes = json.load(response)

    df = create_dataframe()
    #zip_codes["features"][0]["properties"]

    fig = px.choropleth_mapbox(df, geojson=zip_codes, 
                            locations='zip',
                            featureidkey="properties.zip", 
                            color=df[data],
                            title='Economics Indicators by Zip Code',
                            mapbox_style="open-street-map",
                            center={"lat": 41.881832, "lon": -87.623177},
                            color_continuous_scale="Viridis",
                            opacity=0.8,
                            zoom=9)
    
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

if __name__ == '__main__':
    app.run(debug=True)

# alias vsapp='PYTHONPATH=$(pwd) python3 coded_school/Visualization/app.py'