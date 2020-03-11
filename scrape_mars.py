from bs4 import BeautifulSoup
import pandas as pd
import pprint
import requests
import datetime
#import selenium


def scrape():
    ##URLs
    news_url = 'https://mars.nasa.gov/news/'
    jpl_root = 'https://www.jpl.nasa.gov'
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    twiter_url = 'https://twitter.com/marswxreport?lang=en'
    fact_url = 'https://space-facts.com/mars/'
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #make some soups
    news_soup = BeautifulSoup(requests.get(news_url).text, 'html.parser')
    img_soup = BeautifulSoup(requests.get(img_url).text, 'html.parser')
    twit_soup = BeautifulSoup(requests.get(twiter_url).text, 'html.parser')
    fact_soup = BeautifulSoup(requests.get(fact_url).text, 'html.parser')
    hemi_soup = BeautifulSoup(requests.get(hemisphere_url).text, 'html.parser')


    #zip title and description items for iterability
    zipped = zip(
        news_soup.find_all('div', class_='content_title'),
        news_soup.find_all('div', class_='image_and_description_container')
                )

    #loop though zip object and extract data
    articles = []
    for div in zipped:
        info_dict = {
        'article_title' : div[0].a.text.strip(),
        'description_text' : div[1].text.strip(),
        'article_link' : div[1].a['href'].strip(),
        }
        articles.append(info_dict)

    
    images = [] 
    ##get current featured image
    img_dict = {'feat_img_title' : (img_soup.find('div', class_='carousel_items').div.h1.text.strip()),
            'feat_img_url' : jpl_root + str(img_soup.find('div', class_='carousel_items').div.footer.a.attrs['data-fancybox-href'])}

    ##if its a new image, add to image list
    if img_dict not in images:
        images.append(img_dict)


    ## the first tag contains the tweet and the 
    ## second tag contains the date it was posted
    tw_zip = zip(
        twit_soup.find_all('div', class_="js-tweet-text-container"), 
        twit_soup.find_all('span', class_="_timestamp js-short-timestamp")
                )

    weather = []

    ##extract the data and add to weather if not already there
    for tweet in tw_zip:    
        info_dict = {'tweet_text' : tweet[0].p.text,
                    'date' : datetime.date.fromtimestamp(int(tweet[1].attrs['data-time']))}
        if info_dict['tweet_text'].startswith('InSight') and info_dict not in weather:
            weather.append(info_dict)

    ##Extract facts table
    facts_dict = pd.DataFrame(pd.read_html(str(fact_soup))[0]).set_index(0).to_dict()[1]
    ##found a way to get full img URLs without selenium because I was having
    ## trouble with my virtualenv
    ##would like to try with selenium
    hemispheres = []
    img_astrogeology_root = 'https://astropedia.astrogeology.usgs.gov'
    for hemi in hemi_soup.find_all('div', class_='item'):
        info_dict = {
            'title' : hemi.h3.text,
            'full_img_url' : str(img_astrogeology_root + 
                        hemi.a['href'] + 
                        '.tif/full.jpg').replace('search/map', 'download')
        }
        hemispheres.append(info_dict)

    data_dict = {
        'latest_article_title' : articles[0]['article_title'],
        'latest_article_desc' : articles[0]['description_text'],
        'latest_article_link' : f"{news_url}{articles[0]['article_link']}",
        'latest_jpl_img_title' : images[0]['feat_img_title'],
        'latest_jpl_img_url' : images[0]['feat_img_url'],
        'latest_weather_tweet' : weather[0]['tweet_text'],
        'latest_weather_tweet_date' : weather[0]['date'],
        'mars_facts' : facts_dict,
        'hemispheres' : hemispheres

        }

    return data_dict

scrape = scrape()

pprint.pprint(scrape)

