# -*- coding: utf-8 -*-
"""
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import dateutil.parser as dparser
from datetime import date, timedelta
import numpy as np
import re
import time
import pandas as pd

### @param url: takes url of news page of moneycontrol website
### @ returns list of articles on the page
def get_urls_from_page(url):
  try:
     page=requests.get(url) 
  except Exception as e:    
    error_type, error_obj, error_info = sys.exc_info()  
    print (error_type,'ERROR FOR LINK:',url, 'Line:', error_info.tb_lineno) 

  if page.status_code != 200:
    return None

  soup = BeautifulSoup(page.text, "html.parser")
  section = soup.find('section',attrs={'class':'mid-contener contener clearfix'})
  ul = section.find('ul')
  li_tags=ul.find_all('li',attrs={'class':'clearfix'})

  article_urls = []
  for li in li_tags:
    a_tag = li.find('a')
    link = a_tag.get('href')
    article_urls.append(link)

  return article_urls

### @param article : result of requests.get()
### @ returns title,date,description,content of the moneycontrol aritcles
def parse_article(article):
  print("parsing article")
  article = BeautifulSoup(article.text,"html.parser")

  article_title = str(article.find('h1',attrs={'class':'article_title artTitle'}).string)
  article_desc = str(article.find('h2',attrs={'class':'article_desc'}).string)

  article_datetime =  article.find('div',attrs={'class':'article_schedule'})
  article_datetime = article_datetime.span.string + str(article_datetime.contents[2])
  article_datetime = dparser.parse(article_datetime,tzinfos = {"IST": +0})


  article_p_tags = article.find('div',attrs={'class':'content_wrapper arti-flow'}).find_all('p')    

  for p_tag in article_p_tags:
    while p_tag.img is not None:
      p_tag.img.decompose()

    while p_tag.a is not None:
      text = p_tag.a.string
      p_tag.a.replace_with(text)

  article_content = ''.join([str(p_tag.string) for p_tag in article_p_tags])

  return {'title':article_title,
          'datetime':article_datetime,
          'description':article_desc,
          'content':article_content}
  
## getting content of each article
##
##
def main():
  with open('links.txt') as f:
    links = f.readlines()
  f.close()

  print(f"TOTAL LINKS = {len(links)}")
  
  for i in range(len(links)):
    ## parse links to usable form
    link = links[i]
      
    ## get article and save data 1064
    time.sleep(2.5)
    try:
      article = requests.get(links[i])
      row = parse_article(article)
      (pd.Series(row)).to_csv('article_data.csv',mode='a')
      print(f'article {i} added')
    except Exception as e:    
      continue

  
# main()
data = pd.read_csv('article_data.csv')
print(data)