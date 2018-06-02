# Scraping function
def scrape():
    # Import dependencies
    from bs4 import BeautifulSoup as bs
    import requests
    from splinter import Browser
    import tweepy
    from config import consumer_key, consumer_secret, access_token, access_token_secret
    import pandas as pd

    # get_ipython().system('which chromedriver')
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # # NASA Mars News

    # Scrape the NASA Mars News Site and collect the latest News Title 
    # and Paragragh Text. 
    # Assign the text to variables that you can reference later.

    url = "https://mars.nasa.gov/#news_and_events"


    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    # Find first result
    result = soup.find('article', class_='dark_background ms-slide slide-1')

    # Retrieve the thread title
    news_title = result.find('a').text.strip()

    # Retrieve the thread teaser
    news_p = (result.find('div', class_='description').text).split('.')[0].strip()


    # # JPL Mars Space Images - Featured Image

    # Visit the url for JPL's Featured Space Image here.
    page_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    browser.visit(page_url)
    browser.click_link_by_partial_text('FULL IMAGE')

    # Make sure to find the image url to the full size .jpg image.
    # Make sure to save a complete url string for this image.
    # Retrieve page with the requests module
    response = requests.get(page_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    # Find image URL
    image_rel_url = soup.find('a', class_='button fancybox')
    rel_url = image_rel_url['data-fancybox-href']
    partial_url = 'https://www.jpl.nasa.gov/'
    featured_image_url = partial_url + rel_url

    # # Mars Weather
    # Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    # Target User
    target_user = "MarsWxReport"

    # Get all tweets from home feed
    public_tweets = api.user_timeline(target_user)
    # Get the weather tweet text
    mars_weather = public_tweets[0]['text']

    # # Mars Facts

    # Visit the Mars Facts webpage (http://space-facts.com/mars/) 
    # and use Pandas to scrape the table containing 
    # facts about the planet including Diameter, Mass, etc.

    mars_data_url = "https://space-facts.com/mars/"
    tables = pd.read_html(mars_data_url)
    mars_df = tables[0]

    # Rename the column headings
    mars_df.rename(columns={0: 'description', 1: 'value'}, inplace=True)

    # Set the index to "description"
    mars_df.set_index('description', inplace=True)

    # Use Pandas to convert the data to a HTML table string.
    mars_table = mars_df.to_html()

    # # Mars Hemisperes

    # Visit the USGS Astrogeology site here 
    # (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) 
    # to obtain high resolution images for each of Mar's hemispheres.

    # Visit the url for the launch page
    launch_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Retrieve page with the requests module
    response = requests.get(launch_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    # Find first result
    results = soup.find_all('div', class_='item')
    titles = []
    urls = []
    url_prefix = 'https://astrogeology.usgs.gov'

    # Create lists of the img titles
    for result in results:
        titles.append(result.find('div', class_='description').find('h3').text)
        urls.append(url_prefix + result.find('a').attrs['href'])

    # Create lists of the links
    image_urls = []
    for url in urls:
        # Retrieve page with the requests module
        response = requests.get(url)

        # Create BeautifulSoup object; parse with 'html.parser'
        soup = bs(response.text, 'html.parser')

        # Visit each of the pages and extract the image URLs
        browser.visit(url)
        image_urls.append(soup.find('div', class_='downloads').find('a').attrs['href'])

    # Build the list of title-url dictionaries
    hemisphere_image_urls = []
    for i in range(len(titles)):
        hemisphere_image_urls.append("{\"title\": \"" + titles[i] + "\", " +
                                    "\"img_url\": \"" + urls[i] + "\"}")
    
    mars_data = dict([
        ('news_title', news_title),
        ('news_p', news_p),
        ('featured_image_url', featured_image_url),
        ('mars_weather', mars_weather),
        ('mars_table', mars_table),
        ('hemisphere_image_urls', hemisphere_image_urls),
        ('titles', titles),
        ('image_urls', image_urls)
        ])
    return(mars_data)