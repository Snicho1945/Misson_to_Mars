from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # set exec path and initialize chromedriver in splinter
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    # data into dict
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "cerberus": mars_cerb(browser),
        "schiaparelli": mars_schia(browser),
        "syrtis": mars_syrtis(browser),
        "valles_marineris": mars_valles(browser)
    }
    # stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #convert browser html to soup
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # use the parent elem to fin first 'a' tag and save ad 'news_title'
        news_title = slide_elem.find ("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images
def featured_image(browser):

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # find "more info" button and click
    browser.is_element_present_by_text('more info', wait_time=2)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # parse
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:   
        #find relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    
    except AttributeError:
        return None

    # use base url, create absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url

def mars_cerb(browser):

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    full_image_elem = browser.links.find_by_href('/search/map/Mars/Viking/cerberus_enhanced')[1]
    full_image_elem.click()

    # parse
    html = browser.html
    img_soup = soup(html, 'html.parser')

    img_url_rel = img_soup.select_one('ul li a').get("href")

    img_url = img_url_rel
    return img_url

def mars_schia(browser):

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    full_image_elem = browser.links.find_by_href('/search/map/Mars/Viking/schiaparelli_enhanced')[1]
    full_image_elem.click()

    # parse
    html = browser.html
    img_soup = soup(html, 'html.parser')

    img_url_rel = img_soup.select_one('ul li a').get("href")

    img_url = img_url_rel
    return img_url

def mars_syrtis(browser):

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    full_image_elem = browser.links.find_by_href('/search/map/Mars/Viking/syrtis_major_enhanced')[1]
    full_image_elem.click()

    # parse
    html = browser.html
    img_soup = soup(html, 'html.parser')

    img_url_rel = img_soup.select_one('ul li a').get("href")
   
    img_url = img_url_rel
    return img_url

def mars_valles(browser):

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    full_image_elem = browser.links.find_by_href('/search/map/Mars/Viking/valles_marineris_enhanced')[1]
    full_image_elem.click()

    # parse
    html = browser.html
    img_soup = soup(html, 'html.parser')

    img_url_rel = img_soup.select_one('ul li a').get("href")
   
    img_url = img_url_rel
    return img_url

# ## Mars Facts
def mars_facts():

    try:
        # pulling data into a dateframe
        df = pd.read_html('https://space-facts.com/mars/')[0]

    except BaseException:
        return None

    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    return df.to_html(classes="table table-striped")


if __name__ == "__main__":
    # if running as script, print scraped data
    print(scrape_all())