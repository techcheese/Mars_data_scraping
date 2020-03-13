import pymongo
from scrape_class import Mars_Scrape

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_web_scrape

news = db.news

scraped = Mars_Scrape()
scraped_news = scraped.newsScrape()

find_latest = news.find_one(scraped_news)

post_exists = False 


for i in news.find():
    if i['article_title'] == scraped_news['article_title']:
        post_exists = True
    else:
        post_exists = False

if post_exists == False:
    post_id = news.insert_one(scraped_news).inserted_id
    print(post_id)

print(scraped_news)

