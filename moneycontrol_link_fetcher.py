# -*- coding: utf-8 -*-
"""
    
"""

# !pip install html5lib

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta
import time

START_DATE = date(2019,10,1) 
END_DATE = date(2022,8,30)

# article_links = []
base = 'https://www.google.com'
query = ''

####

def get_soup_from_url(url):  
  time.sleep(5)
  webpage = requests.get(url).text
  
  print("Webpage Opened")
  with requests.Session() as c :
    soup = BeautifulSoup (webpage , 'html.parser') 
  
  return soup

#### writes all news article links to txt file
def get_links_from_current_page(soup):
  # print(soup)
  div_tags = soup.find_all('div',attrs={'class':'Gx5Zad fP1Qef xpd EtOod pkphOe'})
  for div in div_tags:
    link = (div.find('a').get('href'))
    # print(link)
    if link.startswith('/url?q=https://www.moneycontrol.com/news/'):
        link = link.split('=')[1].split('&sa')[0]
        file1 = open("links.txt", "a")  
        file1.write(f'{link}\n')
        file1.close()
        print("link added")
    time.sleep(1)
   
####
def get_links_from_next_pages(soup):
  
  ## currrent page links
  get_links_from_current_page(soup)
  
  # tranverse to next page
  next_page_query = soup.find('a',attrs={'aria-label':"Next page", 'class':"nBDE1b G5eFlf"})
  print('Got next page')
  
  if next_page_query != None:
    next_page_url = base + next_page_query.get('href')
    next_soup = get_soup_from_url(next_page_url)
    get_links_from_next_pages(next_soup)

####
def main():
  srt, end = START_DATE, START_DATE + timedelta(7)
  
  while end<END_DATE:
    query = f'/search?q=site:moneycontrol.com+after:{str(srt)}+before:{str(end)}&tbm=nws'
    print(f"getting links for {srt}")
    
    url = base+query
    print(url)
    soup = get_soup_from_url(url) 
    
    get_links_from_next_pages(soup)
      
    srt += timedelta(7)
    end += timedelta(7)


main()