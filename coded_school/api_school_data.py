import json
import lxml.html
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# API Chicago Public School
url_chicago_portal = "https://data.cityofchicago.org/resource/2dn2-x66j.json"

# Fetch data from API
response_API = requests.get(url_chicago_portal)

# Chicago Public Schools - School Progress Reports SY2324
df = pd.read_json(response_API.text)
filtered_df = df[['long_name', 'zip', 'primary_category', 'cps_school_profile', 
                  'mobility_rate_pct', 'chronic_truancy_pct', 'sat_grade_11_score_school', 
                  'college_enrollment_school', 'graduation_5_year_school']]

# Filtered high school
hs_df = filtered_df[filtered_df['primary_category'] == 'HS']

# Get url to CPS school page
for index, row in hs_df.iterrows():
    hs_df.at[index, "cps_school_profile"] = row["cps_school_profile"]["url"]

### Overview page
"""
Get School Grade, Low Income, Diverse Learner, Limited English, Mobility Rate
Chronic Truancy, 
"""
low_income = []
diverse_learners = []
limited_english = []

# Fail in lxml.html
for link in hs_df['cps_school_profile']:
    # At overview page
    r = requests.get(link)
    elem = lxml.html.fromstring(r.text)

    income = elem.xpath("//span[@class='stats-name'][contains(., 'Low  Income')]/following-sibling::div[@class='bar-wrapper']/span[@class='bar-percent']")[0].text_content()
    learners = elem.xpath("//span[@class='stats-name'][contains(., 'Diverse Learners')]/following-sibling::div[@class='bar-wrapper']/span[@class='bar-percent']")[0].text_content()
    english = elem.xpath("//span[@class='stats-name'][contains(., 'Limited English')]/following-sibling::div[@class='bar-wrapper']/span[@class='bar-percent']")[0].text_content()

    low_income.append(income)
    diverse_learners.append(learners)
    limited_english.append(english)

# Try another also fail
low_income = []
diverse_learners = []
limited_english = []

driver = webdriver.Firefox()

for link in hs_df['cps_school_profile']:
    driver.get(link)

    # Wait for the elements to be present
    wait = WebDriverWait(driver, 10)
    income = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='stats-name'][contains(., 'Low  Income')]/following-sibling::div[@class='bar-wrapper']/span[@class='bar-percent']")))
    learners = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='stats-name'][contains(., 'Diverse Learners')]/following-sibling::div[@class='bar-wrapper']/span[@class='bar-percent']")))
    english = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='stats-name'][contains(., 'Limited English')]/following-sibling::div[@class='bar-wrapper']/span[@class='bar-percent']")))

    low_income.append(income.text)
    diverse_learners.append(learners.text)
    limited_english.append(english.text)

driver.quit()



driver.get("https://www.cps.edu/schools/schoolprofiles/609754")

wait = WebDriverWait(driver, 10)
income = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main[1]/section/article/section/section[3]/section[1]/article[2]/div[1]/div/span")))
