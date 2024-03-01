import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('merged_data.csv')
data = data.dropna()

#x = data['student_attainment_rating'].values.reshape(1, -1)
#y1 = data['med_income'].values
#y2 = data['poverty_rate'].values
#y3 = data['unemp_rate'].values
#y4 = data['hs_enrol_rate'].values


#model = LinearRegression()
#model.fit(x, y1)
#print(model.intercept_)
#print(model.coef_)

# Linear Regression: Median Income on Avg SAT score
x = data['sat_grade_11_score_school'].values.reshape(-1, 1)
y = data['med_income'].values
model = LinearRegression().fit(x, y)
print(model.coef_)
print(model.intercept_)
prediction = model.predict(x)

# Scatter plot of Avg SAT Score and Median Income 
plt.scatter(data['sat_grade_11_score_school'], y, c = "green")
plt.plot(data['sat_grade_11_score_school'], prediction, color = "red")
plt.xlabel("Average 11th Grade SAT Score of Schools in Zip Code")
plt.ylabel("Median Househould Income in this Zip Code")
plt.show()