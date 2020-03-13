import pymongo
from scrape_class import Mars_Scrape
from bs4 import BeautifulSoup
import requests

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_web_scrape

news = db.news

scraped = Mars_Scrape()
# scraped_news = scraped.newsScrape()

# find_latest = news.find_one(scraped_news)

# post_exists = False 

# print(f"{find_latest} it exists!")

# for i in news.find():
#     if i['article_title'] == scraped_news['article_title']:
#         post_exists = True
#     else:
#         post_exists = False

# if post_exists == False:
#     post_id = news.insert_one(scraped_news).inserted_id
# else: 
#     post_id = news.find_one(scraped_news)
    
# print(post_id)

# find_latest = news.find_one(scraped_news)

# print(find_latest)


hemi_soup = BeautifulSoup(
    requests.get(scraped.hemisphere_url).text, "html.parser"
)

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
print(scraped.extractHemispheres())