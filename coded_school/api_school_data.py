import pandas as pd
import requests
import numpy as np
from coded_school.data import create_dataframe
from data import create_dataframe

def cleaned_api():
    """
    Retrieves data from the Chicago city portal API, filtering to only High
    Schools in Chicago. Filters the data to include zip code, student attainment
    rating, culture climate rating, transfer rates, absence rates, SAT score,
    dropout rates, and suspension rates. Maps categorical ratings to numerical
    values for stuent attainment and culture cimate rating. Calculates and adds
    a new column for the average dropout rate and suspension rate of years one
    and two.
 
    Returns:
        Cleaned API DataFrame.
    """
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
    """
    Takes the mean of the columns grouped by the specfic zipcode. Fills in all
    na's with the mean of the dataframe.
 
    Inputs:
        df (dataframe): Dataframe
 
    Returns:
        A DataFrame with averaged columns based on zipcode.
    """
    df.fillna(df.mean(), inplace = True)

    avg_df = df.groupby('zip').mean().reset_index()

    return avg_df


def merged_data():
    """
    Calls the average_by_zip() function to get the cleaned api DataFrame with
    averaged columns grouped by zipcode. Also retrieves income data. Merges the
    educational data with the income data based on the zip code.
 
    Returns:
        Merged DataFrame, combining educational and income information.
    """
    data = average_by_zip(clean_columns())
    income = create_dataframe()
    income["log_med_income"] = np.log(income["med_income"])

    data['zip'] = data['zip'].astype(str)

    merged_data = pd.merge(data, income, on = 'zip', how = 'left')
    merged_data.to_csv('./merged_data.csv', index = False)

    return merged_data 
    
if __name__ == '__main__':
    cleaned_data()