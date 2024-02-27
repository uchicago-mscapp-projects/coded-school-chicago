import json
import lxml.html
import pandas as pd
import requests

# API Chicago Public School
url_chicago_portal = "https://data.cityofchicago.org/resource/2dn2-x66j.json"

# Fetch data from API
response_API = requests.get(url_chicago_portal)

# Chicago Public Schools - School Progress Reports SY2324
df = pd.read_json(response_API.text)
# Filtered high school
hs_df = df[df['primary_category'] == 'HS']

filtered_df = hs_df[['long_name', 'zip', 'school_type', 'primary_category', 
                    'student_growth_rating', 'student_attainment_rating', 
                    'culture_climate_rating', 
                    'mobility_rate_pct', 'chronic_truancy_pct', 'sat_grade_11_score_school',
                    'one_year_dropout_rate_year','one_year_dropout_rate_year_1', 
                    'suspensions_per_100_students_1','suspensions_per_100_students_2']]
    #could not find 'school_survery_parent_response_rate_pct'

#Cleaned Data
def clean():
    url_chicago_portal = "https://data.cityofchicago.org/resource/2dn2-x66j.json"
    response_API = requests.get(url_chicago_portal)
    df = pd.read_json(response_API.text)
    
    filtered_df = df[df['primary_category'] == 'HS']
    
    filtered_df = hs_df[['long_name', 'zip', 'school_type', 'primary_category', 
                    'student_growth_rating', 'student_attainment_rating', 
                    'culture_climate_rating', 
                    'mobility_rate_pct', 'chronic_truancy_pct', 'sat_grade_11_score_school',
                    'one_year_dropout_rate_year','one_year_dropout_rate_year_1', 
                    'suspensions_per_100_students_1','suspensions_per_100_students_2']]

    filtered_df['drop_out_rate'] = (filtered_df['one_year_dropout_rate_year'] + filtered_df['one_year_dropout_rate_year_1']) / 2
    filtered_df['suspensions_rate'] = (filtered_df['suspensions_per_100_students_1'] + filtered_df['suspensions_per_100_students_2']) / 2
    filtered_df.drop(['one_year_dropout_rate_year', 'one_year_dropout_rate_year_1',
                      'suspensions_per_100_students_1', 'suspensions_per_100_students_2'], axis = 1, inplace = True)

    return filtered_df
    
# Get url to CPS school page
for index, row in hs_df.iterrows():
    hs_df.at[index, "cps_school_profile"] = row["cps_school_profile"]["url"]