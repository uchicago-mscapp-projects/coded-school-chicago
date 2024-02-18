import sys
import json
import requests
import lxml.html
from lxml.etree import tostring
from bs4 import BeautifulSoup


def get_next_page_url(url):
    """
    This function takes a URL to a page of parks and returns a
    URL to the next page of parks if one exists.

    If no next page exists, this function returns None.

    Parameters:
        * url: a URL to a page of list of parks

    Returns:
        The URL to the next page, if there. If not, will return None.
    """

    #park_list = lxml.html.fromstring(website.text)
    #click_next = park_list.xpath(
        #"//div[@class='open-sans']/div[@id='search-page']/div[@class='container-gs-v2']/div[@class='inner-container-gs-v2']/div[@id='Search-react-component-0a5a6c18-3be0-4cd2-a684-940e9af351b8']/div[@class='search-body list-view']/div[@class='list-map-ad clearfix']/div[@class='pagination-container']/div[@class='pagination-buttons button-group']"
    #)

    website = requests.get(url)
    content = lxml.html.fromstring(website.text)
    div_elements_nothing = content.xpath("////div[@class='search-body list-view']")
    #div_elements_stops = content.xpath("//div[@class='inner-container-gs-v2']")
    
    # Serialize each element to a string
    div_html_contents = [tostring(element, pretty_print=True).decode('utf-8') for element in div_elements]
    return div_html_contents


    #website = requests.get(url)
    #content = lxml.html.fromstring(website.text)
    #return(content)
    #pagination_buttons = content.cssselect(".pagination-buttons.button-group a")
    #return(pagination_buttons)

    #pagination_buttons = school_list.cssselect("div.pagination-buttons.button-group")
    #return(pagination_buttons)
    

    #css select? --- 

    #3 if statements 
    #so pagination-buttons.button-group has 9 anchor-button   anchor-button
    #take the last one 
    #print out the website
    #the last page will give an empty 
    #so if empty return none 

    #next_page_url = click_next[9].get('href') 


    #return next_page_url