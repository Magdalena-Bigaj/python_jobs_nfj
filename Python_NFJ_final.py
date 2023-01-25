#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
from collections import Counter


# In[2]:


def get_page (page):
    r= requests.get('https://nofluffjobs.com/pl/Python?page='+(str(page)))
    c= r.content
    soup= BeautifulSoup (c, 'html.parser')
    return soup
    
def display_technologies(requirements,tech):
    tech_dict = {i: x for i, x in enumerate(Counter(requirements).items())}
    df = pd.DataFrame.from_dict(tech_dict, orient='index', columns=[tech, 'number'])
    pd.set_option('display.max_rows', None)   
    df.sort_values(by=['number'], inplace=True, ascending= False)
    print (df)

def make_dict(list_req):
    return [item.strip() for sublist in list_req for item in sublist]


page= 1
list_req_must=[]
list_req_nice=[]
while True:
    soup= get_page(page)
    if (soup.find('a', {'class': 'jobs-link'}))== None:
        break
    job_sites= soup.find_all('a',{'target':'_self'}, href=True)
    for h in job_sites:
        link= h.get('href')
        if '/job/' in (link):
            try:
                if requests.Response() == 200:
                        break
                r= requests.get('https://nofluffjobs.com/'+(str(link.lstrip('/pl/'))), timeout=1000)
                c= r.content
                soup_job= BeautifulSoup (c, 'html.parser')        
                title= soup_job.find('h1').text
                requirements_must= list(l.text for l in list(soup_job.find_all('ul', {'class': 'mb-0 ng-star-inserted'})))
                rm = list((requirements_must)[0].split("  "))
                list_req_must.append(rm)
                try:
                    requirements_nice_to_have= (str(l.text).strip() for l in (soup_job.find('section', {'id': 'posting-nice-to-have'})))
                    rn= (list(requirements_nice_to_have)[1].split("  "))
                    list_req_nice.append(rn)
                except TypeError as e:    
                    pass
            except Exception as inst:
                print (inst)
    page +=1



display_technologies(make_dict(list_req_must), 'tech- must')
display_technologies(make_dict(list_req_nice), 'tech- nice_to_have')


        

