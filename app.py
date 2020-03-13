from flask import Flask, render_template, jsonify, request
import pymongo
from scrape_class import Mars_Scrape
import pandas as pd
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

    new_scrape = scraped.newsScrape()

    html_table = pd.DataFrame(fact_table, index=[1]).T.to_html()

    return (render_template('heroic_temp.html', 
                            title='MarsFacts',
                            table = html_table, 
                            news_title = new_scrape['article_title'],
                            news_body = new_scrape['description_text'],
                            news_url = new_scrape['article_link'], ))

@app.route('/new_scrape')
def new_scrape():
    news = scraped.newsScrape()
    img = scraped.imgScrape()
    weather = scraped.weatherScrape()



app.run(debug=True)
