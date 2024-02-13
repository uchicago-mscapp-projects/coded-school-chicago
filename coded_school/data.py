import requests
import lxml.html

def get_median_income():
    """
    This function retrieves the zip code data along with its median income and returns it as a dictionary.
    """
    url = "https://zipatlas.com/us/il/chicago/zip-code-comparison/highest-median-household-income.htm"
    r = requests.get(url)
    elem = lxml.html.fromstring(r.text)

    # Get the zip number
    all_zip = elem.xpath("//*[@id='comp']/tbody/tr/td/a")
    zip_code = []
    for row in all_zip:
        z = row.text_content()
        zip_code.append(z)

    # Get median income
    all_med_income = elem.xpath("//*[@id='comp']/tbody/tr/td[3]")
    zip_med_income = []
    for i, row in enumerate(all_med_income):
        income = row.text_content()
        income = int(income.strip('$').replace(",", ""))
        zip_med_income.append((zip_code[i], income))

    dict_zip_income = dict(zip_med_income)

    return dict_zip_income
