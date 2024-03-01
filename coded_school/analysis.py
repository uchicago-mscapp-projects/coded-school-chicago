import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('merged_data.csv')
data = data.dropna()

# Linear Regression: Median Income on Avg SAT score
x = data['sat_grade_11_score_school'].values.reshape(-1, 1)
y = data['med_income'].values
model = LinearRegression().fit(x, y)
print("med_income_intercept:", model.intercept_)
print("sat_coef:", model.coef_)
prediction = model.predict(x)

# Scatter plot of Avg SAT Score and Median Income 
plt.scatter(data['sat_grade_11_score_school'], y, c = "green")
plt.plot(data['sat_grade_11_score_school'], prediction, color = "red")
plt.xlabel("Average 11th Grade SAT Score of Schools in Zip Code")
plt.ylabel("Median Househould Income in this Zip Code")
plt.show()

#Multiple Regression
x1 = data[['student_attainment_rating', 'culture_climate_rating', 
          'mobility_rate_pct', 'chronic_truancy_pct', 'sat_grade_11_score_school',
          'drop_out_rate', 'suspensions_rate']].values
y1 = data['med_income'].values
model1 = LinearRegression().fit(x1, y1)
school_attributes = ['student_attainment_rating', 'culture_climate_rating', 
          'mobility_rate_pct', 'chronic_truancy_pct', 'sat_grade_11_score_school',
          'drop_out_rate', 'suspensions_rate']

for category, coef in zip(school_attributes, model1.coef_):
    print(category, ":", coef)
print("med_income_intercept:", model1.intercept_)