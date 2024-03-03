from dash import Dash, html, dcc, Input, Output
from urllib.request import urlopen
from coded_school.data import *
from coded_school.api_school_data import clean_columns
import statsmodels.api as sm
import plotly.express as px
import numpy as np
import pandas as pd
import dash_table
import json

#zip_codes["features"][0]["properties"]
df_zip_map = create_dataframe()
df_zip_school = pd.read_csv('coded_school/merged_data.csv')
df_zip_school = df_zip_school.fillna(df_zip_school.mean())
df_full_school = clean_columns()

def regression(X, y):
    """
    """
    df_x = df_zip_school[X]
    df_x.insert(0, 'Intercept', 1)
    df_x = df_x.to_numpy()
    df_y = df_zip_school[y].to_numpy().reshape(-1,1)
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

    # Find R-squared
    R_squared = model.rsquared

    # Find F-statistic
    F_statistic = model.fvalue

    return coefficient.T, predicted_value, SE, P_value, R_squared, F_statistic


app = Dash(__name__)

app.layout = html.Div([
    html.H4("Economic indicators for the city of Chicago by zip code"),

    html.Div([
    html.Label("Select X Variable(s):"),
    dcc.Dropdown(
            id='x-dropdown',
            options=[
                {"label": "Student attainment rating", "value": "student_attainment_rating"},
                {"label": "Culture climate rating", "value": "culture_climate_rating"},
                {"label": "Mobility rate (%)", "value": "mobility_rate_pct"},
                {"label": "Chronic truancy (%)", "value": "chronic_truancy_pct"},
                {"label": "SAT grade 11 score", "value": "sat_grade_11_score_school"},
                {"label": "Drop out rate (%)", "value": "drop_out_rate"},
                {"label": "Suspensions rate (%)", "value": "suspensions_rate"}
            ], multi=True, value=["sat_grade_11_score_school", "mobility_rate_pct"] 
        ),

    html.Br(),
    html.Label("Select Y Variable:"),
    dcc.Dropdown(
            id='y-dropdown',
            options=[
                {"label": "Poverty rate (%)", "value": "poverty_rate"},
                {"label": "Unemployment rate (%)", "value": "unemp_rate"},
                {"label": "High school enrollment rate (%)", "value": "hs_enrol_rate"},
                {"label": "Median income ($)", "value": "med_income"},
                {"label": "Log median income", "value": "log_med_income"}
            ], value="med_income"
        ),
        html.Div(id='regression-table-container'),
        html.Div(id='stats-test')
    ]),

    html.Div([
    html.Label("Select X Axis:"),
    dcc.Dropdown(
        id='x-axis',
        options=[
                {"label": "Mobility rate (%)", "value": "mobility_rate_pct"},
                {"label": "Chronic truancy (%)", "value": "chronic_truancy_pct"},
                {"label": "SAT grade 11 score", "value": "sat_grade_11_score_school"},
                {"label": "Suspensions rate (%)", "value": "suspensions_rate"}
        ], value="sat_grade_11_score_school"
    ),

    html.Br(),
    html.Label("Select Y Axis:"),
    dcc.Dropdown(
            id='y-axis',
            options=[
                {"label": "Poverty rate (%)", "value": "poverty_rate"},
                {"label": "Unemployment rate (%)", "value": "unemp_rate"},
                {"label": "Median income ($)", "value": "med_income"},
            ], value="med_income"
        ),
        dcc.Graph(id='scatter-plot'),

    html.Br(),
    html.Label("Select data"),
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
])

@app.callback(
    Output('regression-table-container', 'children'),
    [Input('x-dropdown', 'value'),
     Input('y-dropdown', 'value')]
)
def update_regression_table(selected_x, selected_y):
    if selected_x and selected_y:
        coefficient, _, SE, P_value, R_squared, F_statistic = regression(selected_x, selected_y)

        # Create DataFrame for regression results
        results_df = pd.DataFrame({
            'Variable': ['Intercept'] + selected_x,
            'Coefficient': coefficient[0],
            'Standard Error': SE,
            'P-value': P_value
        })

        # Convert DataFrame to DataTable
        table = dash_table.DataTable(
            id='regression-table',
            columns=[{'name': col, 'id': col} for col in results_df.columns],
            data=results_df.to_dict('records'),
            style_table={'overflowX': 'auto'}
        )

        # Display R-squared and F-statistic
        stats = html.Div([
            html.Label(f'R-squared: {R_squared}'),
            html.Br(),
            html.Label(f'F-statistic: {F_statistic}')
        ])

        return table, stats
    else:
        return html.Div("Please select X and Y variables.")


@app.callback(
    Output("scatter-plot", "figure"),
    [Input("x-axis", "value"),
     Input("y-axis", "value")]
)
def display_scatterplot(x_axis, y_axis):
    fig = px.scatter(df_zip_school, x=x_axis, y=y_axis, trendline="ols")
    return fig


@app.callback(
    Output("graph", "figure"),
    Input("data", "value"))
def display_choropleth(data):
    with urlopen("https://data.cityofchicago.org/api/geospatial/gdcf-axmw?method=export&format=GeoJSON") as response:
        zip_codes = json.load(response)

    fig = px.choropleth_mapbox(df_zip_map, geojson=zip_codes, 
                            locations='zip',
                            featureidkey="properties.zip", 
                            color=df_zip_map[data],
                            title='Economics Indicators by Zip Code',
                            mapbox_style="open-street-map",
                            center={"lat": 41.881832, "lon": -87.623177},
                            color_continuous_scale="Viridis",
                            opacity=0.8,
                            zoom=9)
    
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    sat_score_mean = df_full_school['sat_grade_11_score_school'].mean()
    df_full_school['sat_grade_11_score_school'] = df_full_school['sat_grade_11_score_school'].fillna(sat_score_mean)
    # Create the scatter mapbox plot
    fig.add_trace(px.scatter_mapbox(df_full_school, 
                                    lat="school_latitude", 
                                    lon="school_longitude",
                                    size='sat_grade_11_score_school',
                                    hover_name="long_name", 
                                    hover_data=['student_attainment_rating', 'culture_climate_rating', 
                                                'mobility_rate_pct', 'chronic_truancy_pct', 
                                                'sat_grade_11_score_school']).data[0])
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)

# alias vsapp='PYTHONPATH=$(pwd) python3 coded_school/Visualization/app.py'
    