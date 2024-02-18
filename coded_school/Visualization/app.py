from dash import Dash, html, doc
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children="Chicago's Median Income per zip code"),
    #doc.Graph(figure=px.scatter(df, x="sepal_width", y="sepal_length"))
])

if __name__ == '__main__':
    app.run(debug=True)

# alias vsapp='python3 coded_school/Visualization/app.py'