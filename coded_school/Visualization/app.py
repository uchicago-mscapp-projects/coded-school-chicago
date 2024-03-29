from dash import Dash, html, dcc, Input, Output
from urllib.request import urlopen
from coded_school.Data.income_data import create_dataframe
from coded_school.Data.api_school_data import cleaned_api
import statsmodels.api as sm
import plotly.express as px
import numpy as np
import pandas as pd
import dash_table
import json

# Set up all the data
df_zip_map = create_dataframe()
df_zip_school = pd.read_csv("coded_school/Data/merged_data.csv")
df_zip_school = df_zip_school.fillna(df_zip_school.mean())
df_full_school = cleaned_api()


def regression(X, y):
    """
    This function calculate the multiple linear regression
    and return coefficients, predicted value, and othet test statistics.

    Inputs:
        X (list): A list strings of attributes or dependent variables
        y (str): dependent variable

    Returns:
        coefficients: array of coefficient of the dependent variables.
        predicted_value: predicted result of using the coefficient
                        to estimate data using the training data set.
        SE: Standard error of coefficients.
        P_value: P-value for hypothesis testing.
        R_squared: The R square value of the model.
        F_statistic: The F-statistic of the model.
    """
    # Prepare the data
    df_x = df_zip_school[X]
    df_x.insert(0, "Intercept", 1)
    df_x = df_x.to_numpy()
    df_y = df_zip_school[y].to_numpy().reshape(-1, 1)
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

app.layout = html.Div(
    [
        html.H1(
            "The impact of socioeconomic indicators of an area to school performance metrics",
            style={"textAlign": "center"},
        ),
        html.P(
            "Using data from City of Chicago and ZIP Atlas, we examined how the socioeconomic indicators \
           of a given area impacts school performance metrics. The socioeconomic indicators of interest were: \
           median household income, poverty rate, and unemployment rate. We defined an area by its zip code and, \
           looking only at High Schools, we examined the data of seven performance areas: student attainment,\
           culture/climate, Mobility rate, Chronic truancy, 11th grade SAT score, Drop out rate, and Suspension rate"
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            "Summary of Multiple Regression Analysis",
                            style={"textAlign": "center"},
                        ),
                        html.Label("Select X Variable(s):"),
                        dcc.Dropdown(
                            id="x-dropdown",
                            options=[
                                {
                                    "label": "Student attainment rating",
                                    "value": "student_attainment_rating",
                                },
                                {
                                    "label": "Culture climate rating",
                                    "value": "culture_climate_rating",
                                },
                                {
                                    "label": "Mobility rate (%)",
                                    "value": "mobility_rate_pct",
                                },
                                {
                                    "label": "Chronic truancy (%)",
                                    "value": "chronic_truancy_pct",
                                },
                                {
                                    "label": "SAT grade 11 score",
                                    "value": "sat_grade_11_score_school",
                                },
                                {
                                    "label": "Drop out rate (%)",
                                    "value": "drop_out_rate",
                                },
                                {
                                    "label": "Suspensions rate (%)",
                                    "value": "suspensions_rate",
                                },
                            ],
                            multi=True,
                            value=["sat_grade_11_score_school", "mobility_rate_pct"],
                        ),
                        html.Br(),
                        html.Label("Select Y Variable:"),
                        dcc.Dropdown(
                            id="y-dropdown",
                            options=[
                                {"label": "Poverty rate (%)", "value": "poverty_rate"},
                                {
                                    "label": "Unemployment rate (%)",
                                    "value": "unemp_rate",
                                },
                                {
                                    "label": "High school enrollment rate (%)",
                                    "value": "hs_enrol_rate",
                                },
                                {"label": "Median income ($)", "value": "med_income"},
                                {
                                    "label": "Log median income",
                                    "value": "log_med_income",
                                },
                            ],
                            value="med_income",
                        ),
                        html.Div(id="regression-table-container"),
                        html.Div(id="stats-test"),
                    ],
                    style={"width": "49%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        html.H2(
                            "Choropleth Map by Zip Code", style={"textAlign": "center"}
                        ),
                        html.Label("Select Data"),
                        dcc.RadioItems(
                            id="data",
                            options=[
                                {"label": "Poverty rate (%)", "value": "poverty_rate"},
                                {
                                    "label": "Unemployment rate (%)",
                                    "value": "unemp_rate",
                                },
                                {
                                    "label": "High school enrollment rate (%)",
                                    "value": "hs_enrol_rate",
                                },
                                {"label": "Median income ($)", "value": "med_income"},
                            ],
                            value="med_income",
                            inline=True,
                        ),
                        dcc.Graph(id="graph"),
                    ],
                    style={"width": "49%", "float": "right", "display": "inline-block"},
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div(
            [
                html.H2(
                    "OLS Visualization",
                    style={"textAlign": "center", "marginBottom": "0px"},
                ),
                html.Label("Select X Axis:"),
                dcc.Dropdown(
                    id="x-axis",
                    options=[
                        {"label": "Mobility rate (%)", "value": "mobility_rate_pct"},
                        {
                            "label": "Chronic truancy (%)",
                            "value": "chronic_truancy_pct",
                        },
                        {
                            "label": "SAT grade 11 score",
                            "value": "sat_grade_11_score_school",
                        },
                        {"label": "Suspensions rate (%)", "value": "suspensions_rate"},
                    ],
                    value="sat_grade_11_score_school",
                ),
                html.Br(),
                html.Label("Select Y Axis:"),
                dcc.Dropdown(
                    id="y-axis",
                    options=[
                        {"label": "Poverty rate (%)", "value": "poverty_rate"},
                        {"label": "Unemployment rate (%)", "value": "unemp_rate"},
                        {"label": "Median income ($)", "value": "med_income"},
                    ],
                    value="med_income",
                ),
                dcc.Graph(id="scatter-plot"),
            ],
            style={"margin": "0px", "padding": "0px"},
        ),
    ]
)


@app.callback(
    Output("regression-table-container", "children"),
    [Input("x-dropdown", "value"), Input("y-dropdown", "value")],
)
def update_regression_table(selected_x, selected_y):
    """
    This function will update the table according to the input data.

    Inputs:
        selected_x: a list of dependent variables.
        selected_y: a dependent variable

    Returns:
        The update table and the R square and F test statistics.
    """
    if selected_x and selected_y:
        coefficient, _, SE, P_value, R_squared, F_statistic = regression(
            selected_x, selected_y
        )

        # Format numbers to have exactly 6 digits
        coeff6 = [np.round(c, 6) for c in coefficient[0]]
        SE6 = [np.round(s, 6) for s in SE]
        P6 = [np.round(p, 6) for p in P_value]
        R6 = np.round(R_squared, 6)
        F6 = np.round(F_statistic, 6)

        # Create DataFrame for regression results
        results_df = pd.DataFrame(
            {
                "Variable": ["Intercept"] + selected_x,
                "Coefficient": coeff6,
                "Standard Error": SE6,
                "P-value": P6,
            }
        )

        # Convert DataFrame to DataTable
        table = dash_table.DataTable(
            id="regression-table",
            columns=[{"name": col, "id": col} for col in results_df.columns],
            data=results_df.to_dict("records"),
            style_table={"overflowX": "auto"},
        )

        # Display R-squared and F-statistic
        stats = html.Div(
            [
                html.Label(f"R-squared: {R6}"),
                html.Br(),
                html.Label(f"F-statistic: {F6}"),
            ]
        )

        return table, stats
    else:
        return html.Div("Please select X and Y variables.")


@app.callback(
    Output("scatter-plot", "figure"),
    [Input("x-axis", "value"), Input("y-axis", "value")],
)
def display_scatterplot(x_axis, y_axis):
    """
    This function creates a scatter plot and shows the regression line between two variables.

    Inputs:
        x_axis: independent variable
        y_value: dependent variable

    Returns: a Scatter plot
    """
    fig = px.scatter(
        df_zip_school, x=x_axis, y=y_axis, color=x_axis, trendline="ols"
    )
    return fig


@app.callback(Output("graph", "figure"), Input("data", "value"))
def display_choropleth(data):
    """
    This function will return the choropleth map of various economic indicators
    of the city of Chicago divided by zip code.

    Inputs:
        data (str): The value in which the map will show.

    Returns: A map separated by zip code
    """
    # Get the map boundary data
    with urlopen(
        "https://data.cityofchicago.org/api/geospatial/gdcf-axmw?method=export&format=GeoJSON"
    ) as response:
        zip_codes = json.load(response)

    fig = px.choropleth_mapbox(
        df_zip_map,
        geojson=zip_codes,
        locations="zip",
        featureidkey="properties.zip",
        color=df_zip_map[data],
        title="Economics Indicators by Zip Code",
        mapbox_style="open-street-map",
        center={"lat": 41.85267, "lon": -87.66373},
        color_continuous_scale="Viridis",
        opacity=0.8,
        zoom=9,
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # Prepare the individual high school information
    sat_score_mean = df_full_school["sat_grade_11_score_school"].mean()
    df_full_school["sat_grade_11_score_school"] = df_full_school[
        "sat_grade_11_score_school"
    ].fillna(sat_score_mean)

    # Create the scatter mapbox plot
    fig.add_trace(
        px.scatter_mapbox(
            df_full_school,
            lat="school_latitude",
            lon="school_longitude",
            hover_name="long_name",
            hover_data=[
                "student_attainment_rating",
                "culture_climate_rating",
                "mobility_rate_pct",
                "chronic_truancy_pct",
                "sat_grade_11_score_school",
            ],
            color_discrete_sequence=["red"],
        )
        .update_traces(marker=dict(size=10, opacity=0.5))
        .data[0]
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)

# alias vsapp='PYTHONPATH=$(pwd) python3 coded_school/Visualization/app.py'
