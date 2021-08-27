# Import Splinter and Beautiful Soup and other dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last modified": dt.datetime.now(),
        "hemispheres": hem_data(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

### Featured Article

def mars_news(browser):
    # Visit the Mars/Nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Set up parent element
        slide_elem = news_soup.select_one('div.list_text')
        # Find title of article
        slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

### Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Find and click the "Full Image" button
    full_image_element = browser.find_by_tag('button')[1]
    full_image_element.click()

    # Parse the resulting HTML with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image URL
        image_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{image_url_rel}'

    return img_url

### Mars Facts

def mars_facts():
    try:
        # Use read_html to scrape info from table and set as pandas df
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
   
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes='table table-striped')

### Mars Hemispheres

def hem_data(browser):
    # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
    ## Hemispheres
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
        hemisphere_dict = {'img_url': img_url, 'title': title}
        hemisphere_image_urls.append(hemisphere_dict)
        browser.back()
    
    # Close the browser after scraping
    browser.quit()
    
    return hemisphere_image_urls
        
if __name__ == '__main__':
        # If running as script, print scraped data
        print(scrape_all())
