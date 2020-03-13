from flask import Flask, render_template, jsonify, request
import pymongo
from scrape_class import Mars_Scrape
import pandas as pd
from bson.objectid import ObjectId

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_web_scrape

LAST_DATA = db.latest_data

def conditional_insert(post, tag, collection = LAST_DATA):
    ("""" 
    DOCSTRING

    collection = mongo_db collection
    post = post to be inserted into database
    tag = key in a post we want to check fo runiqueness

    The purpose of this function is to avoid clutter in the database from repeated 
    running of the code collection.insert_one() or collection.insert_many() 
    every time we test the code

    The functions return the post_id if a new post is made
    or
    returns a (2,) tuple containing the assigned id of an exisiting post and the post_flag 
    variable which should return Falsey since the flag will only be raised if the post passed
    is a unique post

    could potentially improve the accuracy by checking the amount of tags that are equal
    repeated post should only have the _id tag not equal
    
    """)
    post_flag = False 
    for i in collection.find():
        if i[tag] == post[tag]:
            post_flag = True
        else:
            post_flag = False

    if post_flag == False:
        ### to add datetime inserted do dict1.update(dict2)
        post_id = collection.insert_one(post).inserted_id
    
        return str(post_id)

    else: 
        exists_id = collection.find_one(post)['_id']

        return (exists_id, post_flag)

NEWS = db.news
IMGS = db.images
TWIT = db.twitter_weather
EXT_DATA = db.extracted_data
LAST_DATA = db.latest_data



@app.route('/')
def landing():
    scraped = Mars_Scrape()
    
    fact_table = scraped.extractFactTable()
  
    table_insert = conditional_insert(
        collection=EXT_DATA, 
        post=fact_table, 
        tag = 'Equatorial Diameter:'
        )
    html_table = pd.DataFrame(EXT_DATA.find_one(table_insert[0]), index=[1]).T.to_html()

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
