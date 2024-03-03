import pandas as pd
import requests
from coded_school.data import create_dataframe
import numpy as np

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

    growth_mapping = {'Far Below Average': 1, 'Below Average': 2, 'Average': 3, 'Above Average': 4, 'Far Above Average': 5}
    attainment_mapping = {'Far Below Expectations': 1, 'Below Average': 2, 'Average': 3, 'Above Average': 4, 'Met Expectations': 5, 'Far Above Expectations': 6}
    climate_mapping = {'Not Enough Data': pd.NA, 'Well Organized': 5, 'Organized': 4, 'Moderately Organized': 3, 'Partially Organized': 2, 'Not Yet Organized': 1}

    filtered_df['student_growth_rating'] = filtered_df.replace(filtered_df['student_growth_rating'], growth_mapping)
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
    
    filtered_df = filtered_df[['zip', 'student_attainment_rating', 
                    'culture_climate_rating', 'mobility_rate_pct', 'chronic_truancy_pct', 
                    'sat_grade_11_score_school','one_year_dropout_rate_year','one_year_dropout_rate_year_1', 
                    'suspensions_per_100_students_1','suspensions_per_100_students_2', 'school_latitude', 'school_longitude', 'long_name']]

    attainment_mapping = {'FAR BELOW EXPECTATIONS': 1, 'BELOW AVERAGE': 2, 'AVERAGE': 3, 'ABOVE AVERAGE': 4, 'MET EXPECTATIONS': 5, 'FAR ABOVE EXPECTATIONS': 6}
    climate_mapping = {'NOT ENOUGH DATA': None, 'WELL ORGANIZED': 5, 'ORGANIZED': 4, 'MODERATELY ORGANIZED': 3, 'PARTIALLY ORGANIZED': 2, 'NOT YET ORGANIZED': 1}

    filtered_df['student_attainment_rating'] = filtered_df['student_attainment_rating'].map(attainment_mapping)
    filtered_df['culture_climate_rating'] = filtered_df['culture_climate_rating'].map(climate_mapping)

    filtered_df['drop_out_rate'] = (filtered_df['one_year_dropout_rate_year'] + filtered_df['one_year_dropout_rate_year_1']) / 2
    filtered_df['suspensions_rate'] = (filtered_df['suspensions_per_100_students_1'] + filtered_df['suspensions_per_100_students_2']) / 2
    filtered_df.drop(['one_year_dropout_rate_year', 'one_year_dropout_rate_year_1',
                      'suspensions_per_100_students_1', 'suspensions_per_100_students_2'], axis = 1, inplace = True)

    return filtered_df

def average_by_zip(df):
    df.fillna(df.mean(), inplace = True)

    avg_df = df.groupby('zip').mean().reset_index()

    return avg_df


def cleaned_data():
        data = average_by_zip(clean_columns())
        income = create_dataframe()
        income["log_med_income"] = np.log(income["med_income"])

        data['zip'] = data['zip'].astype(str)

        merged_data = pd.merge(data, income, on = 'zip', how = 'left')
        merged_data.to_csv('./merged_data.csv', index = False)
        return merged_data 
    
if __name__ == '__main__':
    cleaned_data()