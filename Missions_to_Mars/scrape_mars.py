#**************************************************************************************************#
# Import Dependencies
#**************************************************************************************************#
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from splinter import Browser

#**************************************************************************************************#
# Initialize Browser (Chrome Driver)
    # @NOTE: Be sure to replace the path with the actual path to chromedriver (OS dependant)
#**************************************************************************************************#
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

#**************************************************************************************************#
# Scrape Mars Data
#**************************************************************************************************#
def scrape():
    browser = init_browser()
    #------------------------------------------------#
    # NASA Mars News
    #------------------------------------------------#
    # URL of page to be scraped
    mars_news_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_news_url)

    # Wait 3 seconds before proceeding to give browser time to fully load
    time.sleep(3)

    # Create BeautifulSoup object & parse with 'html.parser'
    mars_news_html_text = browser.html
    mars_news_soup = BeautifulSoup(mars_news_html_text, 'html.parser')

    # Mars News Headline Title
    news_hl_title = mars_news_soup.find('div', class_='list_text').find('div', class_='content_title').text

    # Mars News Headline Teaser Paragraph
    news_teaser_p = mars_news_soup.find('div', class_='list_text').find('div', class_='article_teaser_body').text

    #------------------------------------------------#
    # JPL Mars Space Images - Featured Image
    #------------------------------------------------#
    # URL of page to be scraped
    jpl_base_url = 'https://www.jpl.nasa.gov'
    jpl_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_image_url)

    # Wait 3 seconds before proceeding to give browser time to fully load
    time.sleep(3)

    # Create BeautifulSoup object & parse with 'html.parser'
    jpl_image_html_text = browser.html
    jpl_image_soup = BeautifulSoup(jpl_image_html_text, 'html.parser')

    # Use split() to extract the portion of the url needed, setting to variable for later use
    jpl_image_extra_path = jpl_image_soup.find('article', class_="carousel_item")['style'].split("url('")[1].split("');")[0]

    # Another way: using Splinter and browser.find_by_xpath:
    # Set jpl_featured_image_xpath to XPath copied from Chrome inspector tool
    # jpl_featured_image_xpath = '//*[@id="page"]/section[1]/div/div/article'

    # Pass variable through to spliter browser.find_by_xpath method, traverse to ['style']
    # browser.find_by_xpath(jpl_featured_image_xpath)['style']

    # Use split to extract the portion of the url needed, setting to variable for later use
    # jpl_image_extra_path2 = browser.find_by_xpath(jpl_featured_image_xpath)['style'].split('url("')[1].split('");')[0]

    # Set image path to be a concat of jpl_base_url + jpl_image_extra_path
    featured_image_url = f'{jpl_base_url}{jpl_image_extra_path}'
    # featured_image_url2 = f'{jpl_base_url}{jpl_image_extra_path2}'

    # Find featured image title within the article tag setting to variable for later use
    featured_image_title = jpl_image_soup.find('article', class_="carousel_item")['alt']

    #------------------------------------------------#
    # Mars Weather
    #------------------------------------------------#
    # URL of page to be scraped
    mars_wx_twitter_url = 'https://twitter.com/marswxreport?lang=en'
    # browser.visit(mars_wx_twitter_url)

    # # Wait 3 seconds before proceeding to give browser time to fully load
    # time.sleep(3)

    # # Create BeautifulSoup object & parse with 'html.parser'
    # mars_wx_twitter_html_text = browser.html
    # mars_wx_twitter_soup = BeautifulSoup(mars_wx_twitter_html_text, 'html.parser')

    # # Using browser.visit()
    # mars_wx_tweets = mars_wx_twitter_soup.find_all('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")

    # # Iterate through Mars Weather tweets one by one, searching for <span> holding tweet text
    # for mars_wx_tweet in mars_wx_tweets:
        
    #     # Set variable to tweet text
    #     mars_wx_wx_tweet = mars_wx_tweet.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text
        
    #     # Remove unwanted charaters (pic link, if they exist at end of tweet), use split() to pull them off
    #     mars_wx_wx_tweet = mars_wx_wx_tweet.split('pic.twitter.com/')[0]
    #     mars_wx_wx_tweet = mars_wx_wx_tweet.replace('\n',' ')
    #     print(mars_wx_wx_tweet)
        
    #     # Determine if tweet is weather related and exit, else pass and move on to next tweet
    #     if 'InSight sol ' in mars_wx_wx_tweet:
    #         break
    #     else:
    #         pass

    # Using requests.get 
    mars_wx_response = requests.get(mars_wx_twitter_url)
    mars_wx_twitter_soup = BeautifulSoup(mars_wx_response.text, 'html.parser')

    # Print formatted verion of BeautifulSoup object to examine
    # print(mars_wx_twitter_soup2.prettify())

    mars_wx_tweets = mars_wx_twitter_soup.find_all('div', class_="js-tweet-text-container")

    # Iterate through Mars Weather tweets one by one, searching for <p> holding tweet text
    for mars_wx_tweet in mars_wx_tweets:
        
        # Set variable to tweet text
        mars_wx_wx_tweet = mars_wx_tweet.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
        
        # Remove unwanted charaters (pic link, if they exist at end of tweet), use split() to pull them off
        mars_wx_wx_tweet = mars_wx_wx_tweet.split('pic.twitter.com/')[0]
        mars_wx_wx_tweet = mars_wx_wx_tweet.replace('\n',' ')
        print(mars_wx_wx_tweet)
        
        # Determine if tweet is weather related and exit, else pass and move on to next tweet
        if 'InSight sol ' in mars_wx_wx_tweet:
            break
        else:
            pass

    # Set first weather related tweet to required variable
    mars_weather = mars_wx_wx_tweet

    #------------------------------------------------#
    # Mars Facts
    #------------------------------------------------#
    # URL of page to be scraped
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)

    # Wait 3 seconds before proceeding to give browser time to fully load
    time.sleep(3)

    # Create BeautifulSoup object & parse with 'html.parser'
    mars_facts_html_text = browser.html
    mars_facts_soup = BeautifulSoup(mars_facts_html_text, 'html.parser')

    # Using Splinter and browser.find_by_xpath:
    # Set mars_facts_table_xpath to XPath copied from Chrome inspector tool
    mars_facts_table_xpath = '//*[@id="tablepress-p-mars-no-2"]'

    # Pass variable through to spliter browser.find_by_xpath method
    mars_facts_table_html = browser.find_by_xpath(mars_facts_table_xpath).html

    # Add <table> tag around mars_facts_table_html to use in pd.read_html()
    mars_facts_table_html = f'<table> {mars_facts_table_html} </table>'

    # Read in the mars_facts_table_html html table into a pandas DataFrame
    mars_facts_df = pd.read_html(mars_facts_table_html)[0]

    # Set first column as the DataFrame index, removed column header name and rename 2nd column
    mars_facts_df = mars_facts_df.set_index(0)
    mars_facts_df = mars_facts_df.rename_axis('')
    mars_facts_df = mars_facts_df.rename(columns={1:'Value'})

    # Use to_html method to create html table from mars_facts_df DataFrame
    mars_facts_html_table = mars_facts_df.to_html()

    # # Remove unwanted charaters ('\n')
    # mars_facts_html_table = mars_facts_html_table.replace('\n',' ')

    #------------------------------------------------#
    # Mars Hemispheres
    #------------------------------------------------#
    # URL of page to be scraped
    mars_hemispheres_base_url = 'https://astrogeology.usgs.gov'
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)

    # Wait 3 seconds before proceeding to give browser time to fully load
    time.sleep(3)

    # Create BeautifulSoup object & parse with 'html.parser'
    mars_hemispheres_html_text = browser.html
    mars_hemispheres_soup = BeautifulSoup(mars_hemispheres_html_text, 'html.parser')

    # Create dictionary to hold all of Mars Hemisphere key: value pairs for title and img_url
    hemisphere_image_urls = []

    # Iterate through the mars_hemispheres_soup html to find needed elements
    for hemisphere in mars_hemispheres_soup.find_all('div', class_='item'):
        # Locate and set variable for Hemisphere Name/title and use .split() to remove ' Enhanced'
        title = hemisphere.find('div', class_='description').find('h3').text.split(' Enhanced')[0]
        
        # Locate and set variable for Hemisphere's individual url (concat to mars_hemispheres_base_url)
        hemisphere_url_extra_path = hemisphere.find('div', class_='description').find('a')['href']
        hemisphere_url = f'{mars_hemispheres_base_url}{hemisphere_url_extra_path}'
        
        # Navigate spliter's browser to each hemisphere's url to scrape that hemisphere's full resolution image url
        browser.visit(hemisphere_url)

        # Wait 3 seconds before proceeding to give browser time to fully load
        time.sleep(3)
        
        # Create BeautifulSoup object & parse with 'html.parser'
        hemisphere_html_text = browser.html
        hemisphere_soup = BeautifulSoup(hemisphere_html_text, 'html.parser')
        
        # Locate and set variable for each hemisphere's individual full resolution image url
        hemisphere_img_url = hemisphere_soup.find('div', class_='downloads').find('li').find('a')['href']
        
        # Create a dictionary holding the Hemisphere's Name/title & it's full resolution image url
        hemisphere_image_dict = {'title': title, 'img_url': hemisphere_img_url}
        
        # Append hemisphere_image_urls dictionary to include Name/title and full resolution image url
        hemisphere_image_urls.append(hemisphere_image_dict)

    #------------------------------------------------#
    # Store all of the scraped data in a dictionary
    #------------------------------------------------#
    mars_data = {
        'news_hl_title': news_hl_title,
        'news_teaser_p': news_teaser_p,
        'featured_image_url': featured_image_url,
        'featured_image_title': featured_image_title,
        'mars_weather': mars_weather,
        'mars_facts_html_table': mars_facts_html_table,
        'hemisphere_image_urls': hemisphere_image_urls
        }

    #------------------------------------------------#
    # Close the browser window opened by splinter
    #------------------------------------------------#
    browser.quit()

    #------------------------------------------------#
    # Return Results
    #------------------------------------------------#
    return mars_data