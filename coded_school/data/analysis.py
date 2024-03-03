import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import statsmodels.formula.api as smf

data = pd.read_csv('merged_data.csv')
data = data.dropna()

# Linear Regression: Median Income on Avg SAT score
model = smf.ols(formula='med_income ~  sat_grade_11_score_school', data = data).fit()
print(model.summary())

# Median Income on School Attributes
model2 = smf.ols(formula = 'med_income ~ student_attainment_rating + culture_climate_rating + mobility_rate_pct + chronic_truancy_pct + sat_grade_11_score_school + drop_out_rate + suspensions_rate', data = data).fit()
print(model2.summary())

# Poverty Rate on School Attributes
model3 = smf.ols(formula = 'poverty_rate ~ student_attainment_rating + culture_climate_rating + mobility_rate_pct + chronic_truancy_pct + sat_grade_11_score_school + drop_out_rate + suspensions_rate', data = data).fit()
print(model3.summary())

# Unemployment Rate on School Attributes
model4 = smf.ols(formula = 'unemp_rate ~ student_attainment_rating + culture_climate_rating + mobility_rate_pct + chronic_truancy_pct + sat_grade_11_score_school + drop_out_rate + suspensions_rate', data = data).fit()
print(model4.summary())

# Med Income vs SAT 
fig = px.scatter(data, x = 'sat_grade_11_score_school', 
                 y = 'med_income', 
                 hover_data = ['zip'],  color = 'med_income')
fig.show()

# Med Income vs SAT w/ trendline
fig2 = px.scatter(data, x = 'sat_grade_11_score_school', 
                 y = 'med_income', 
                 hover_data = ['zip'], color = 'med_income',
                 trendline = 'ols',)
fig2.show()

# poverty rate vs SAT 
fig3 = px.scatter(data, x = 'sat_grade_11_score_school', 
                 y = 'poverty_rate', 
                 hover_data = ['zip'], color = 'poverty_rate',
                 trendline = 'ols')
fig3.show()

# poverty rate vs suspensions
fig4 = px.scatter(data, x = 'suspensions_rate', 
                 y = 'poverty_rate', 
                 hover_data = ['zip'], color = 'poverty_rate')
fig4.show()

# unemp rate vs chronic truancy
fig4 = px.scatter(data, x = 'chronic_truancy_pct', 
                 y = 'unemp_rate', 
                 hover_data = ['zip'], color = 'unemp_rate',)
fig4.show()

# unemp rate vs suspensions
fig5 = px.scatter(data, x = 'suspensions_rate', 
                 y = 'unemp_rate', 
                 hover_data = ['zip'], color = 'unemp_rate',)
fig5.show()
