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
    This function retrieves the zip code data along with its median income and returns it as a dictionary.
    """
    r = requests.get(url)
    elem = lxml.html.fromstring(r.text)

    # Get the zip number
    all_zip = elem.xpath("//*[@id='comp']/tbody/tr/td/a")
    zip_code = []
    for row in all_zip:
        z = row.text_content()
        zip_code.append(z)

    # Get geo data
    all_data = elem.xpath("//*[@id='comp']/tbody/tr/td[3]")
    zip_data = []
    for i, row in enumerate(all_data):
        income = row.text_content()
        zip_data.append((zip_code[i], income))

    dict_zip_data = dict(zip_data)

    return dict_zip_data


def combine_dicts(dicts_list):
    all_keys = set()
    for d in dicts_list:
        all_keys.update(d.keys())  # Collect all unique keys

    combined_dict = {}
    for key in all_keys:
        combined_dict[key] = []  # Initialize empty list for each key
        for d in dicts_list:
            combined_dict[key].append(d.get(key))  # Append value if key exists, otherwise append None
    return combined_dict


def create_data_frame(urls):
    dicts_list = []
    for web in urls:
        dict_zip = get_geo_data(web)
        dicts_list.append(dict_zip)
    combine = combine_dicts(dicts_list)
    df = pd.DataFrame.from_dict(combine, orient='index', columns=col_name)
    return df