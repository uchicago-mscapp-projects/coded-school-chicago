import json
import lxml.html
import pandas as pd
import requests
from data import get_geo_data, combine_dicts, create_dataframe

# API Chicago Public School
url_chicago_portal = "https://data.cityofchicago.org/resource/2dn2-x66j.json"

# Fetch data from API
response_API = requests.get(url_chicago_portal)

#Chicago Public Schools - School Progress Reports SY2324
df = pd.read_json(response_API.text)
#Filtered high school
hs_df = df[df['primary_category'] == 'HS']

filtered_df = hs_df[['long_name', 'zip', 'school_type', 'primary_category', 
                    'student_growth_rating', 'student_attainment_rating', 
                    'culture_climate_rating', 
                    'mobility_rate_pct', 'chronic_truancy_pct', 'sat_grade_11_score_school',
                    'one_year_dropout_rate_year','one_year_dropout_rate_year_1', 
                    'suspensions_per_100_students_1','suspensions_per_100_students_2']]
    #could not find 'school_survery_parent_response_rate_pct'

#Cleaned Data
def keep():
    url_chicago_portal = "https://data.cityofchicago.org/resource/2dn2-x66j.json"
    response_API = requests.get(url_chicago_portal)
    df = pd.read_json(response_API.text)
    
    filtered_df = df[df['primary_category'] == 'HS']
    
    filtered_df = filtered_df[['long_name', 'zip', 'school_type', 'primary_category', 
                    'student_growth_rating', 'student_attainment_rating', 
                    'culture_climate_rating', 
                    'mobility_rate_pct', 'chronic_truancy_pct', 'sat_grade_11_score_school',
                    'one_year_dropout_rate_year','one_year_dropout_rate_year_1', 
                    'suspensions_per_100_students_1','suspensions_per_100_students_2']]

    #loop find unique value -- 1 2 3 

    growth_mapping = {'Far Below Average': 1, 'Below Average': 2, 'Average': 3, 'Above Average': 4, 'Far Above Average': 5}
    attainment_mapping = {'Far Below Expectations': 1, 'Below Average': 2, 'Average': 3, 'Above Average': 4, 'Met Expectations': 5, 'Far Above Expectations': 6}
    climate_mapping = {'Not Enough Data': pd.NA, 'Well Organized': 5, 'Organized': 4, 'Moderately Organized': 3, 'Partially Organized': 2, 'Not Yet Organized': 1}

    filtered_df['student_growth_rating'] = filtered_df.replace(filter_df['student_growth_rating'], growth_mapping)
    filtered_df['student_attainment_rating'] = filtered_df['student_attainment_rating'].replace(attainment_mapping)
    filtered_df['culture_climate_rating'] = filtered_df['culture_climate_rating'].replace(climate_mapping)

    filtered_df['drop_out_rate'] = (filtered_df['one_year_dropout_rate_year'] + filtered_df['one_year_dropout_rate_year_1']) / 2
    filtered_df['suspensions_rate'] = (filtered_df['suspensions_per_100_students_1'] + filtered_df['suspensions_per_100_students_2']) / 2
    filtered_df.drop(['one_year_dropout_rate_year', 'one_year_dropout_rate_year_1',
                      'suspensions_per_100_students_1', 'suspensions_per_100_students_2'], axis = 1, inplace = True)

    return filtered_df

def clean_columns():
    url_chicago_portal = "https://data.cityofchicago.org/resource/2dn2-x66j.json"
    response_API = requests.get(url_chicago_portal)
    df = pd.read_json(response_API.text)
    
    filtered_df = df[df['primary_category'] == 'HS']
    
    filtered_df = filtered_df[['zip', 'student_growth_rating', 'student_attainment_rating', 
                    'culture_climate_rating', 'mobility_rate_pct', 'chronic_truancy_pct', 
                    'sat_grade_11_score_school','one_year_dropout_rate_year','one_year_dropout_rate_year_1', 
                    'suspensions_per_100_students_1','suspensions_per_100_students_2']]

    growth_mapping = {'Far Below Average': 1, 'Below Average': 2, 'Average': 3, 'Above Average': 4, 'Far Above Average': 5}
    attainment_mapping = {'Far Below Expectations': 1, 'Below Average': 2, 'Average': 3, 'Above Average': 4, 'Met Expectations': 5, 'Far Above Expectations': 6}
    climate_mapping = {'Not Enough Data': pd.NA, 'Well Organized': 5, 'Organized': 4, 'Moderately Organized': 3, 'Partially Organized': 2, 'Not Yet Organized': 1}

    filtered_df['student_growth_rating'] = filtered_df['student_growth_rating'].replace(growth_mapping)
    filtered_df['student_attainment_rating'] = filtered_df['student_attainment_rating'].replace(attainment_mapping)
    filtered_df['culture_climate_rating'] = filtered_df['culture_climate_rating'].replace(climate_mapping)

    filtered_df['drop_out_rate'] = (filtered_df['one_year_dropout_rate_year'] + filtered_df['one_year_dropout_rate_year_1']) / 2
    filtered_df['suspensions_rate'] = (filtered_df['suspensions_per_100_students_1'] + filtered_df['suspensions_per_100_students_2']) / 2
    filtered_df.drop(['one_year_dropout_rate_year', 'one_year_dropout_rate_year_1',
                      'suspensions_per_100_students_1', 'suspensions_per_100_students_2'], axis = 1, inplace = True)

    return filtered_df

def average_by_zip():
    data = clean_columns()

    unique_zips = numpy.unique[data['zip']]
    
#Get url to CPS school page
for index, row in hs_df.iterrows():
    hs_df.at[index, "cps_school_profile"] = row["cps_school_profile"]["url"]


def cleaned_data():
        data = clean()
        income = create_dataframe()

        frames = [data, income]

        merged_data = pd.concat(frames)

        return merged_data 