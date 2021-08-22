# Import Splinter and Beautiful Soup and other dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# ### Featured Article

# Visit the Mars/Nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Set up HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')

# Set up parent element
slide_elem = news_soup.select_one('div.list_text')

# Find title of article
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com/'
browser.visit(url)

# Find and click the "Full Image" button
full_image_element = browser.find_by_tag('button')[1]
full_image_element.click()

# Parse the resulting HTML with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image URL
image_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')
image_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{image_url_rel}'

# ### Mars Facts

# Scrape info from table and set as pandas df
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# Put table back in html
df.to_html()

browser.quit()


