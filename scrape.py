# -*- coding: utf-8 -*-
"""
Created on Wed May  2 16:21:54 2018

@author: Andre
"""

'web scrape with picture and Yelp'
__author__ = 'Andrew Liu'

#%%
from bs4 import BeautifulSoup
import requests

url = 'https://brickset.com/sets?query=2016'
item = requests.get(url)
soup = BeautifulSoup(item.content,'lxml')
        
#%%
print(soup.prettify()[1000:3000])
#%%
import re
set_name = soup.find_all('a', href = re.compile('sets'))
imgs = soup.find_all('a', class_="highslide plain mainimg")
#imgs = soup.find_all('img', src = re.compile('images'))
#%%
names = []
links = []
for set_n in set_name:
    names.append(set_n.get_text())
    
for img in imgs:
    links.append(img.get('href'))
#%%
print(names)

#%%
print(links)

#%%
titles = []
for name in names:
    name = name.split(':')
    if len(name)==2:
        titles.append(name[1].strip())

        

#%%
path = r'C:\Users\Andre\Dropbox\Economics\programming\python\Scrap\output\cover'+'\\'+names[0]+'.jpg'
for i in range(len(names)):
    pic = requests.get(links[i]).content
    pic_path = r'C:\Users\Andre\Dropbox\Economics\programming\python\Scrap\output\cover'+'\\'+names[i]+'.jpg'
    with open(pic_path,'wb') as f:
        f.write(pic)
        
#%%
url = 'https://www.yelp.com/search?find_desc=restaurants&find_loc=santa+barbara'
item = requests.get(url)
soup = BeautifulSoup(item.content,'lxml')

#%%
restaurants = soup.find_all('a', class_= 'biz-name js-analytics-click')
print(restaurants)


#%%
from selenium import webdriver
#import requests
#from selenium.webdriver.common.action_chains import ActionChains
#import time
#import os

path_to_extension = r'D:\Dropbox\Economics\programming\python\Scrap\1.16.2_0'
option = webdriver.ChromeOptions()
option.add_argument('load-extension=' + path_to_extension)
#option.add_argument('--incognito')

browser = webdriver.Chrome(executable_path=r'D:\Dropbox\Economics\programming\python\Scrap\chromedriver', chrome_options=option)

#%%
browser.get('https://www.yelp.com/search?find_desc=restaurants&find_loc=santa+barbara&start=0&attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2,RestaurantsPriceRange2.4,RestaurantsPriceRange2.3')

#%%
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
     
browser.get('https://www.yelp.com/search?find_desc=restaurants&find_loc=santa+barbara&start=0&attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2,RestaurantsPriceRange2.4,RestaurantsPriceRange2.3')

timeout = 20
try:
    # Wait until the final element [Avatar link] is loaded.
    # Assumption: If Avatar link is loaded, the whole page would be relatively loaded because it is among
    # the last things to be loaded.
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, './/input[@class="js-redo-search-checkbox"]')))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

#%%
restaurants = browser.find_elements_by_xpath('.//div[@class="search-result natural-search-result"]//a[@class="biz-name js-analytics-click"]')
dollar_signs = browser.find_elements_by_xpath('.//div[@class="search-result natural-search-result"]//span[@class="business-attribute price-range"]')
rating_pics = browser.find_elements_by_xpath('.//div[@class="search-result natural-search-result"]//img[contains(@src,"stars.png")]')
review_counts = browser.find_elements_by_xpath('.//div[@class="search-result natural-search-result"]//span[@class="review-count rating-qualifier"]')
address_disps = browser.find_elements_by_xpath('.//div[@class="search-result natural-search-result"]//address')

assert (len(restaurants)==len(dollar_signs)==len(rating_pics)==len(review_counts)==len(address_disps)==10)
#print(restaurants)
#len(restaurants)

#%%
names = []
prices = []
ratings = []
reviews = []
addresses = []
for i in range(10):
    names.append(restaurants[i].text)
    prices.append(dollar_signs[i].text)
    ratings.append(rating_pics[i].text)
    reviews.append(review_counts[i].text)
    addresses.append(address_disps[i].text)
#%%
print(addresses)
addresses[0].split('\n')

#%%
next_page = browser.find_element_by_xpath('.//a[contains(@class,"next")]')
next_page.click()

#%%
browser.get('https://www.yelp.com/search?find_desc=restaurants&find_loc=santa+barbara&start=0&attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2,RestaurantsPriceRange2.4,RestaurantsPriceRange2.3')

timeout = 20
try:
    # Wait until the final element [Avatar link] is loaded.
    # Assumption: If Avatar link is loaded, the whole page would be relatively loaded because it is among
    # the last things to be loaded.
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, './/input[@class="js-redo-search-checkbox"]')))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()
#%%
import time
#next_page = browser.find_element_by_xpath('.//a[contains(@class,"next")]')
page_no = browser.find_element_by_xpath('.//div[@class="page-of-pages arrange_unit arrange_unit--fill"]')
page_no = int(page_no.text.split('of')[1].strip())
names = [[]]*page_no
prices = [[]]*page_no
ratings = [[]]*page_no
reviews = [[]]*page_no
addresses = [[]]*page_no
#%%
start_page = 0
current_page = start_page
end_page = 3

#%%
while current_page < end_page:
    try:
        browser.get('https://www.yelp.com/search?find_desc=restaurants&find_loc=santa+barbara&start='+str(10*current_page)+'&attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2,RestaurantsPriceRange2.4,RestaurantsPriceRange2.3')

        timeout = 20
        try:
            # Wait until the final element [Avatar link] is loaded.
            # Assumption: If Avatar link is loaded, the whole page would be relatively loaded because it is among
            # the last things to be loaded.
            WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, './/input[@class="js-redo-search-checkbox"]')))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()
        restaurants = browser.find_elements_by_xpath('.//div[@class="search-result natural-search-result"]//a[@class="biz-name js-analytics-click"]')
        dollar_signs = browser.find_elements_by_xpath('.//div[@class="search-result natural-search-result"]//span[@class="business-attribute price-range"]')
        rating_pics = browser.find_elements_by_xpath('.//div[@class="search-result natural-search-result"]//img[contains(@src,"stars.png")]')
        review_counts = browser.find_elements_by_xpath('.//div[@class="search-result natural-search-result"]//span[@class="review-count rating-qualifier"]')
        address_disps = browser.find_elements_by_xpath('.//div[@class="search-result natural-search-result"]//div[@class="secondary-attributes"]')
        assert (len(restaurants)==len(address_disps))
        if len(review_counts) != len(restaurants) or len(rating_pics) != len(restaurants):
            print('Page '+str(current_page+1)+' needs inspection')
            current_page += 1
        else:
            print('Page '+str(current_page+1)+' analysis complete')
            get_name = []
            get_price = []
            get_address = []
            get_rating = []
            get_review = []
            for i in range(len(restaurants)):
                get_name.append(restaurants[i].text)
                get_price.append(dollar_signs[i].text)
                get_address.append(address_disps[i].text)
                get_rating.append(rating_pics[i].text)
                get_review.append(review_counts[i].text)
            names[current_page] = get_name
            prices[current_page] = get_price
            addresses[current_page] = get_address
            ratings[current_page] = get_rating
            reviews[current_page] = get_review
            print('Page '+str(current_page+1)+' data extraction done.')
            current_page += 1
            time.sleep(1)
    except:
        raise

