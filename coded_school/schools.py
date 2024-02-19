import requests
import lxml.html
import csv

def scrape_school_page(url_list):
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
  for url in url_list: 
    response = requests.get(url)
    root = lxml.html.fromstring(response.text)
    
    school_page_info = {}
    name = root.cssselect('div.class:contains("name")')
    school_page_info['name'] = name[0].text_content().strip()
    
    address = root.cssselect('section div div section div div div div div div div')
    address = address[6].text_content().strip()
    zip = zip.split()
    zip = zip[-1]
    school_page_info['zip'] = zip
  
    avg_sat = root.cssselect('div.class:contains("score") + div.class')
    school_page_info['avg_sat'] = avg_sat[0].text_content().strip()

    #ap_math 
    #ap_science
    #other_ap
    #school_page_info['ap_participation'] = ap_math + ap_science + other_ap
    
    grad_rate = root.cssselect('section.id' + 'div.class:contains("percentage")')
    school_page_info['grad_rate'] = grad_rate[0].text_content().strip()
    
    low_inc_perc = root.cssselect('section.class' + 'div.class:contains("percentage")')
    school_page_info['low_inc_perc'] = low_inc_perc[0].text_content().strip()
    
    ratio = root.cssselect('section div div section div div')
    school_page_info['stu_to_teach'] = ratio[0].text_content().strip()
    
    absent = root.cssselect('body div section div section div div')
    absent = 
    school_page_info['absenteeism'] = asbent[].text_content().strip()
    
    return school_page_info
    
  
  
  
        
  