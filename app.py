from flask import Flask, render_template, jsonify, request, redirect
import pymongo
from scrape_class import Mars_Scrape
import pandas as pd
from bson.objectid import ObjectId

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_web_scrape

NEWS = db.news
IMGS = db.images
TWIT = db.twitter_weather
EXT_DATA = db.extracted_data
LAST_DATA = db.latest_data


def conditional_insert(post, tag, collection=LAST_DATA):
    (
        """" 
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
    
    """
    )

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
        exists_id = collection.find_one(post)["_id"]

        return (exists_id, post_flag)


@app.route("/")
def landing():
    scraped = Mars_Scrape()

    fact_table = scraped.extractFactTable()

    table_insert = conditional_insert(
        collection=EXT_DATA, post=fact_table, tag="Equatorial Diameter:"
    )

    html_table = pd.DataFrame(EXT_DATA.find_one(table_insert[0]), index=[1]).T.to_html()

    new_scrape = scraped.newsScrape()

    news_insert = conditional_insert(
        collection=NEWS, post=new_scrape, tag="article_title"
    )

    if isinstance(news_insert, tuple):
        latest_news = NEWS.find_one(news_insert[0])

    elif isinstance(news_insert, str):
        latest_news = NEWS.find_one(ObjectId(news_insert))

    img_scrape = scraped.imgScrape()

    img_insert = conditional_insert(
        collection=IMGS, post=img_scrape, tag="feat_img_title"
    )

    if isinstance(img_insert, tuple):
        latest_img = IMGS.find_one({"_id": ObjectId(img_insert[0])})

    elif isinstance(img_insert, str):
        latest_img = IMGS.find_one({"_id": ObjectId(img_insert)})

    weather_scrape = scraped.weatherScrape()

    weather_insert = conditional_insert(
        collection=TWIT, post=weather_scrape, tag="tweet_text"
    )

    if isinstance(weather_insert, tuple):
        latest_weather = TWIT.find_one({"_id": ObjectId(weather_insert[0])})

    elif isinstance(weather_insert, str):
        latest_weather = TWIT.find_one({"_id": ObjectId(weather_insert)})

    hemi1 = scraped.extractHemispheres()[0]

    return render_template(
        "heroic_temp.html",
        title="MarsFacts",
        table=html_table,
        news_title=latest_news["article_title"],
        news_body=latest_news["description_text"],
        news_url=latest_news["article_link"],
        img_title=latest_img["feat_img_title"],
        img_url=latest_img["feat_img_url"],
        weather_text=latest_weather["tweet_text"],
        date_added=latest_weather["date"],
        twitter_url=scraped.twiter_url,
        hemi1_title=hemi1["title"],
        hemi1_link=hemi1["hemi_link"],
        hemi1_url=hemi1["full_img_url"],
    )

@app.route('/hemispheres')
def hemi():
    scraped = Mars_Scrape()
    hemis = scraped.extractHemispheres()
    hemi1 = hemis[0]
    hemi2 = hemis[1]
    hemi3 = hemis[2]
    hemi4 = hemis[3]


    return(
        render_template('full_width_temp.html',
            hemi1_title = hemi1['title'],
            hemi1_link = hemi1['hemi_link'],
            hemi1_url = hemi1['full_img_url'],
            hemi2_title = hemi2['title'],
            hemi2_link = hemi2['hemi_link'],
            hemi2_url = hemi2['full_img_url'],
            hemi3_title = hemi3['title'],
            hemi3_link = hemi3['hemi_link'],
            hemi3_url = hemi3['full_img_url'],
            hemi4_title = hemi4['title'],
            hemi4_link = hemi4['hemi_link'],
            hemi4_url = hemi4['full_img_url'],

        )
    )

@app.route('/scrape')
def scrape():
    fact_insert = scraped.extractFactTable()
    new_scrape = scraped.newsScrape()
    weather_scrape = scraped.weatherScrape()
    img_scrape = scraped.imgScrape()
    hemi1 = scraped.extractHemispheres()[0]

    fact_insert = conditional_insert(
        collection=EXT_DATA, post=fact_insert, tag="Equatorial Diameter:"
    )
    news_insert = conditional_insert(
        collection=NEWS, post=new_scrape, tag="article_title"
    )
    
    img_insert = conditional_insert(
        collection=IMGS, post=img_scrape, tag="feat_img_title"
    )

    weather_insert = conditional_insert(
        collection=TWIT, post=weather_scrape, tag="tweet_text"
    )

    return redirect('/')

app.run(debug=True)
