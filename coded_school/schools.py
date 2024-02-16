import requests
import lxml.html

def scrape_school_page(url):
  """
  This function takes a Url to a high school page, from Great Schools,
  and returns a dictionary with School Name, ACT scores, AP Participation, IB enrollment,
  Graduation Rate, low-Income student percentage, student to teacher ratio, 
  and chronically absent percentage of the school.

  Paramters: 
    * url: url to a school page

  Returns: 
   A dictionary with the following keys:
            * name: the name of the school
            * zip: school zip code
            * avg_sat: average SAT score
            * ap_participation: percent of students participating in AP scores
            * ib_enrollment: percent of students enrolled in IB
            * grad_rate: graduation rate of the school
            * low_income_per: percentage of students who qualify for free-reduced lunch
            * student_to_teacher: student to teacher ratio
            * absenteeism: percentage of students who are chronically absent 
  """
  response = requests.get(url)
  root = lxml.html.fromstripoetry ng(response.text)
  
  school_page_info = {}
  
  name = root.cssselect('div.class:contains("name")')
  school_page_info['name'] = name[0].text_content()
  
  avg_sat = root.cssselect()
  school_page_info['act_avg'] = act_avg[0].text_content()
        
  