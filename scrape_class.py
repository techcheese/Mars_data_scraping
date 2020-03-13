from bs4 import BeautifulSoup
import pandas as pd
import pprint
import requests
import datetime


class Mars_Scrape:
    def __init__(self):
        self.news_url = "https://mars.nasa.gov/news/"

        self.jpl_root = "https://www.jpl.nasa.gov"
        self.img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

        self.twiter_url = "https://twitter.com/marswxreport?lang=en"

        self.fact_url = "https://space-facts.com/mars/"

        self.hemisphere_url_root = 'https://astrogeology.usgs.gov'
        self.hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


    def newsScrape(self):
        news_soup = BeautifulSoup(requests.get(self.news_url).text, "html.parser")

        title = (news_soup.find("div", class_="content_title"),)
        desc = news_soup.find("div", class_="image_and_description_container")
        info_dict = {
            "article_title": title[0].a.text.strip(),
            "description_text": desc.text.strip(),
            "article_link": str(self.news_url) + str(desc.a["href"].strip()),
        }

        return info_dict

    def imgScrape(self):
        img_soup = BeautifulSoup(requests.get(self.img_url).text, "html.parser")

        img_dict = {
            "feat_img_title": (
                img_soup.find("div", class_="carousel_items").div.h1.text.strip()
            ),
            "feat_img_url": str(self.jpl_root)
            + str(
                img_soup.find("div", class_="carousel_items").div.footer.a.attrs[
                    "data-fancybox-href"
                ]
            ),
        }

        return img_dict

    def weatherScrape(self):
        twit_soup = twit_soup = BeautifulSoup(
            requests.get(self.twiter_url).text, "html.parser"
        )

        tweet = (twit_soup.find("div", class_="js-tweet-text-container"),)
        tweet_time = twit_soup.find("span", class_="_timestamp js-short-timestamp")

        info_dict = {
            "tweet_text": tweet[0].p.text,
            "date": datetime.date.fromtimestamp(int(tweet_time.attrs["data-time"])).strftime("%m/%d/%Y"),
        }

        return info_dict

    def extractFactTable(self):
        fact_soup = BeautifulSoup(requests.get(self.fact_url).text, "html.parser")

        facts_dict = pd.DataFrame(pd.read_html(str(fact_soup))[0]).set_index(0).to_dict()[1]

        return facts_dict

    def extractHemispheres(self):
        hemi_soup = BeautifulSoup(
            requests.get(self.hemisphere_url).text, "html.parser"
        )
        hemispheres = []
        img_astrogeology_root = 'https://astropedia.astrogeology.usgs.gov'
        for hemi in hemi_soup.find_all('div', class_='item'):
            info_dict = {
                'title' : hemi.h3.text,
                'hemi_link' : str(self.hemisphere_url_root) + 
                    hemi.a['href'],
                'full_img_url' : str(img_astrogeology_root + 
                            hemi.a['href'] + 
                            '.tif/full.jpg').replace('search/map', 'download')
            }
            hemispheres.append(info_dict)

        return hemispheres

    def scrapeLatest(self):
        news = self.newsScrape()
        imgs = self.imgScrape()
        weather = self.weatherScrape()

        data_dict = {
        'latest_article_title' : news['article_title'],
        'latest_article_desc' : news['description_text'],
        'latest_article_link' : f"{self.news_url}{news['article_link']}",
        'latest_jpl_img_title' : imgs['feat_img_title'],
        'latest_jpl_img_url' : imgs['feat_img_url'],
        'latest_weather_tweet' : weather['tweet_text'],
        'latest_weather_tweet_date' : weather['date'],}

        return data_dict