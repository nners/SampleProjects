# Scraping listings of items sold from a popular Armenian website (similar to Ebay) 

# packages 
import requests
from bs4 import BeautifulSoup
import pandas as pd


# we will need to install this package --> the point is to make sure that we are change our agentclass every time
from fake_useragent import UserAgent 

base_url = """https://www.list.am/category/{categ}/{page}"""

item_url = """https://www.list.am/item/{item_num}"""

browser = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


html_parsed = BeautifulSoup(result.content, 'html.parser')


class CategoryParser():
   
    
    """ Class for parsing through the categories in list.am. 
        Inputs are the url, browser & page_number - note that 
        we need a browser in order to avoid having issues with 
        cloudflare  """
    
    def __init__(self,base_url,item_url,browser):
        self.base_url = base_url
        self.browser = browser
        self.item_url = item_url
        
    #   Method for getting the html for a given category and page
    #   Note that different categories will have different # of total pages
        
    def get_html(self, category, page_number):
        result = requests.get(self.base_url.format(categ = category, page = page_number) , headers=self.browser)
        html_parsed = BeautifulSoup(result.content, 'html.parser')
        return html_parsed
    
    # Method for getting html of an item page
    
    def visit_item(self, item):
        result = requests.get(self.item_url.format(item_num = item) , headers=self.browser)
        html_parsed = BeautifulSoup(result.content, 'html.parser')
        return html_parsed
    
    # Getting the list of all class names 
    
    def get_all_classes(self):
        classes = []
        for element in self.find_all(class_=True):
            classes.extend(element["class"])
        classes = list(dict.fromkeys(classes)) # dedupe the class list 
        return classes


# Inputing the base url along with the fake browser --> make sure to change thr browser

# There are 212 categories right now with the first category being category = 2 

list_am_instance = CategoryParser(base_url=base_url, browser=browser, item_url=item_url)

page_example = list_am_instance.get_html(category=16, page_number=1)

page_example

page_content = page_example.find_all('div', id = 'contentr')[0]  

item_info = page_content.find_all('a',href = True)


item_id = []
content_price = []
content_comment = []
content_category = []
content_posted_date = []
content_specific_date = []
for i in item_info: 
    item_id.append(i.get('href').split('/')[2])
    content_price.extend([i.text for i in (i.find_all('div', class_ = 'p'))])
    content_category.extend([i.text for i in (i.find_all('div', class_ = 'c'))])
    content_comment.extend([i.text for i in (i.find_all('div', class_ = 'u'))])
    content_posted_date.extend([i.text for i in (i.find_all('div', class_ = 'd'))])
    content_specific_date.extend([i.text for i in (i.find_all('div', class_ = 'at'))])
    
data = {
  'item_id': list(filter(lambda x: len(x)>3, item_id)),  # This is to make sure we are getting an item ID
                                                            # Sometimes the returned value is not an item ID
  'content_price': content_price,
    'content_comment': content_comment,
    'content_category': content_category,
    'content_posted_date': content_posted_date,
    'content_specific_date': content_specific_date   
}

data # Everything together

data['item_id'] # The item_id 


# example of going to an item page  13234864 --> we can loop through the results in data
list_am_instance = CategoryParser(base_url=base_url,item_url=item_url, browser=browser)
list_am_instance.visit_item(item=15131536)
