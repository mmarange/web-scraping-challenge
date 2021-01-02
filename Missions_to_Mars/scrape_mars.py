def scrape():

    #!/usr/bin/env python
    # coding: utf-8

    # In[21]:


    import pandas as pd
    from splinter import Browser
    from bs4 import BeautifulSoup
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support.ui import WebDriverWait
    import pymongo
    import requests
    import time

    # In[6]:


    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # # NASA Mars News

    # In[7]:


    url = 'https://mars.nasa.gov/news'

    # Retrieve page with the requests module
    browser.visit(url)
    time.sleep(5) # Sleep for 5 seconds
    html = browser.html
   
    # Create BeautifulSoup object; parse with 'html.parser'
    news_soup = BeautifulSoup(html, 'html.parser')
    

    # Retrieve the parent divs for all articles
    articles = news_soup.find("li", class_ = "slide")
    news_title = articles.find('div', class_='content_title').text
    news_p = articles.find('div', class_='article_teaser_body').text


    # # JPL Mars Space Images - Featured Image

    # In[9]:


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Retrieve page with the requests module
    browser.visit(url)
    time.sleep(5) # Sleep for 5 seconds
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    image_soup = BeautifulSoup(html, 'html.parser')
    browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(5) # Sleep for 5 seconds
    # # Create BeautifulSoup object; parse with 'html.parser' for the full image page
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    #frame = image_soup.find("div", class_ = 'fancybox-lock')
    image = image_soup.find("img", class_ = "fancybox-image")['src']

    base_url = 'https://www.jpl.nasa.gov'
    image_link = f'{base_url}{image}'
    image_link


    # # Mars Facts

    # In[10]:


    url = 'https://space-facts.com/mars/'


    # In[11]:


    tables = pd.read_html(url)


    # In[12]:


    description = tables[0]
    description.columns = ["Description", "Mars"]
    description


    # In[14]:


    description_html = description.to_html(index=False, border=0, classes = 'table table-striped')
    description_html


    # # Mars Hemispheres

    # In[15]:


    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # Retrieve page with the requests module
    browser.visit(url)
    html = browser.html

    #Use Beautiful soup to find Hemisphere titles in text
    elements_soup = BeautifulSoup(html, 'html.parser')
    elements_div = elements_soup.find("div", class_ = "collapsible")
    elements = elements_div.find_all("h3")
    elements = [element.text for element in elements]
    elements


    # In[16]:


    # Use Splinter to click each title and scrap for the full hemisphere image

    hemisphere_image_urls = [] # empty list to be appended by dictionaries

    for x in range(len(elements)): #parse for each title element
        
        browser.links.find_by_partial_text(f'{elements[x]}').click()
        
        title = elements[x]
        image_url = browser.find_by_css('a').links.find_by_partial_text("Sample")['href']
        
        hemisphere_image_urls.append(
                                        {"title": f'{title}', "img_url": f'{image_url}'}
                                    )
    #return to home page
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        html = browser.html
        


    # In[17]:


    browser.quit()


    # In[19]:


    dict_final = {"news_title":news_title,
                "news_p":news_p,
                "featured_image": image_link,
                "table": description_html,
                "hemispheres":hemisphere_image_urls      
                }
    return (dict_final)


