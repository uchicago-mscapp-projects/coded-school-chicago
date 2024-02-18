from dash import Dash, html, dcc, Output
import plotly.express as px
from coded_school.data import get_median_income
#from ..data import get_median_income
from urllib.request import urlopen
import pandas as pd
import json

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children="Chicago's Median Income per zip code"),
    html.Div(dcc.Graph(id='graph'))
])

@app.callback(
    Output("graph", "figure"))
def display_choropleth():
    with urlopen("https://data.cityofchicago.org/api/geospatial/gdcf-axmw?method=export&format=GeoJSON") as response:
        zip_codes = json.load(response)

    income_dict = get_median_income()
    income_data = pd.DataFrame.from_dict(income_dict, orient='index', columns=['Median'])
    income_data = income_data.reset_index()
    income_data = income_data.rename(columns={'index': 'Zips'})

    #zip_codes["features"][0]["properties"]

    map_zip = px.choropleth(income_data, geojson=zip_codes, 
                            locations='Zips',
                            featureidkey="properties.zip", 
                            color='Median',
                            projection="mercator",
                            title='Median Income by Zip Code',
                            labels={'Median': 'Median income'})
    
    map_zip.update_geos(fitbounds="locations", visible=False)
    map_zip.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return map_zip

if __name__ == '__main__':
    app.run(debug=True)

# alias vsapp='PYTHONPATH=$(pwd) python3 coded_school/Visualization/app.py'