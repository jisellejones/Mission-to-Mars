#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and Beautiful Soup and other dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Featured Article

# In[3]:


# Visit the Mars/Nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Set up HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')

# Set up parent element
slide_elem = news_soup.select_one('div.list_text')

# Find title of article
slide_elem.find('div', class_='content_title')


# In[5]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[6]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[7]:


# Visit URL
url = 'https://spaceimages-mars.com/'
browser.visit(url)


# In[8]:


# Find and click the "Full Image" button
full_image_element = browser.find_by_tag('button')[1]
full_image_element.click()


# In[9]:


# Parse the resulting HTML with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[10]:


# Find the relative image URL
image_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')
image_url_rel


# In[11]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{image_url_rel}'


# ### Table of Information

# In[12]:


# Scrape info from table and set as pandas df
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[13]:


# Put table back in html
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.    
for x in range(0, 4):
    full_image_elem = browser.links.find_by_partial_text('Enhanced')[x].click()
    html = browser.html
    html_soup = soup(html, "html.parser")
    img_url_part = html_soup.find('li').a['href']
    img_url = f'{url}{img_url_part}'
    title = html_soup.find('h2', class_='title').text
    hemisphere_dict = {'img_url': img_url,
                       'title': title}
    hemisphere_image_urls.append(hemisphere_dict)
    browser.back()


# In[16]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[17]:


# 5. Quit the browser
browser.quit()

