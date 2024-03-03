from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from coded_school.data import *
from coded_school.api_school_data import clean_columns
from urllib.request import urlopen
import json

#zip_codes["features"][0]["properties"]
df_zip_ino = create_dataframe()
df_zip_school = pd.read_csv('coded_school/merged_data.csv')
df_full_school = clean_columns()

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
        ], value="med_income", inline=True
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

    # Create the scatter mapbox plot
    fig.add_trace(px.scatter_mapbox(df_full_school, 
                                    lat="school_latitude", 
                                    lon="school_longitude",
                                    size="sat_grade_11_score_school", 
                                    hover_name="long_name", 
                                    hover_data=['student_attainment_rating', 'culture_climate_rating', 
                                                'mobility_rate_pct', 'chronic_truancy_pct', 
                                                'sat_grade_11_score_school']).data[0])
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)

# alias vsapp='PYTHONPATH=$(pwd) python3 coded_school/Visualization/app.py'
    
def regression(X, y):
    df = pd.read_csv('coded_school/merged_data.csv')
    df = df.fillna(df.mean())
    df_x = df[X]
    df_x.insert(0, 'Intercept', 1)
    df_x = df_x.to_numpy()
    df_y = df[y].to_numpy().reshape(-1,1)
    model = sm.OLS(df_y, df_x).fit()

    # Find coefficients
    coefficient = (np.linalg.inv(df_x.T @ df_x) @ df_x.T) @ df_y

    # Find predicted values
    projection_matrix = (df_x @ np.linalg.inv(df_x.T @ df_x)) @ df_x.T
    predicted_value = projection_matrix @ df_y

    # Find standard error of coefficients
    SE = model.bse

    # Find p-value
    P_value = model.pvalues

    # Find R square
    R_sq = model.rsquared

    return coefficient.T, predicted_value, SE, P_value, R_sq