import requests
import lxml.html
import pandas as pd

url_poverty_rate = "https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-family-poverty.htm"
url_unemp_rate = "https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-unemployment-rate.htm"
url_hs_enroll_rate = "https://zipatlas.com/us/il/chicago/zip-code-comparison/percentage-enrolled-in-high-school.htm"
url_med_income = "https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-median-household-income.htm"

urls = [url_poverty_rate, url_unemp_rate, url_hs_enroll_rate, url_med_income]
col_name = ["poverty_rate", "unemp_rate", "hs_enrol_rate", "med_income"]


def get_geo_data(url):
    """
    This function retrieves the zip code data its associate the values 
    and returns it as a dictionary.

    Inputs:
        url (str): url website to retrieve data

    Returns:
        Dictionary mapping zipcode to its value
    """
    r = requests.get(url)
    elem = lxml.html.fromstring(r.text)

    # Get the zip number
    all_zip = elem.xpath("//table[@id='comp']/tbody/tr/td/a")
    zip_code = []
    for row in all_zip:
        z = row.text_content()
        zip_code.append(z)

    # Get geo data
    all_data = elem.xpath("//table[@id='comp']/tbody/tr/td[3]")
    zip_data = []
    for i, row in enumerate(all_data):
        income = row.text_content()
        zip_data.append((zip_code[i], income))

    dict_zip_data = dict(zip_data)

    return dict_zip_data


def combine_dicts(dicts_list):
    """
    Combines a list of dictionaries into a single dictionary where each key maps to a list of cleaned and transformed values.
    
    Parameters:
        dicts_list (list): A list of dictionaries.
    
    Returns:
        A dictionary where each key maps to a list of cleaned and transformed values from the input dictionaries.
    """
    all_keys = set()
    # Collect all unique keys
    for d in dicts_list:
        all_keys.update(d.keys())  
    combined_dict = {}
    for key in all_keys:
        # Initialize empty list for each key
        combined_dict[key] = []  
        for d in dicts_list:
            value = d.get(key)
            # Clean and transform value to float
            if value:
                value = float(value.strip("%$").replace(",", ""))
            combined_dict[key].append(value)
    return combined_dict


def create_dataframe():
    """
    Creates a DataFrame containing geographic values for Chicago based on its zip codes.

    Inputs:
        urls (list): A list of URLs.

    Returns:
        A DataFrame containing geographic values per zip code.
    """
    urls = [url_poverty_rate, url_unemp_rate, url_hs_enroll_rate, url_med_income]
    dicts_list = []
    for web in urls:
        dict_zip = get_geo_data(web)
        dicts_list.append(dict_zip)
    combine = combine_dicts(dicts_list)
    df = pd.DataFrame.from_dict(combine, orient='index', columns=col_name)
    # Convert median income to integer
    df["med_income"] = df["med_income"].astype("int")
    df = df.reset_index()
    df = df.rename(columns={'index': 'Zips'})
    return df