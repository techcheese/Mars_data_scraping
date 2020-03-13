from flask import Flask, render_template, jsonify, request
import pymongo
from scrape_class import Mars_Scrape
import pandas as pd

from bson.objectid import ObjectId

#import jinja2

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_web_scrape

NEWS = db.news
IMGS = db.images
TWIT = db.twitter_weather




@app.route('/')
def landing():
    scraped = Mars_Scrape()
    
    fact_table = scraped.extractFactTable()
    html_table = pd.DataFrame(fact_table, index=[1]).T.to_html()


    new_scrape = scraped.newsScrape()

    post_exists = False 
    for i in NEWS.find():
        if i['article_title'] == new_scrape['article_title']:
            post_exists = True
        else:
            post_exists = False

    if post_exists == False:
        ### to add datetime inserted do dict1.update(dict2)
        post_id = NEWS.insert_one(new_scrape).inserted_id
    else: 
        post_id = NEWS.find_one(new_scrape)['_id']

    latest_news = NEWS.find_one({'_id' : ObjectId(post_id) })

    latest_img = scraped.imgScrape()

    latest_weather = scraped.weatherScrape()

    hemi1 = scraped.extractHemispheres()[0]

    return (render_template('heroic_temp.html', 
                            title='MarsFacts',
                            table = html_table, 
                            news_title = latest_news['article_title'],
                            news_body = latest_news['description_text'],
                            news_url = latest_news['article_link'], 
                            img_title = latest_img['feat_img_title'],
                            img_url = latest_img['feat_img_url'],
                            weather_text = latest_weather['tweet_text'],
                            date_added = latest_weather['date'],
                            twitter_url = scraped.twiter_url,
                            hemi1_title = hemi1['title'],
                            hemi1_link = hemi1['hemi_link'],
                            hemi1_url = hemi1['full_img_url'],
                            ))

@app.route('/new_scrape')
def new_scrape():
    news = scraped.newsScrape()
    img = scraped.imgScrape()
    weather = scraped.weatherScrape()



app.run(debug=True)
