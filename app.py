from flask import Flask, render_template, jsonify, request
from scrape_class import Mars_Scrape
app = Flask(__name__)

@app.route('/')
def landing():
    scraped = Mars_Scrape()
    news = scraped.newsScrape()
    imgs = scraped.imgScrape()
    weather = scraped.weatherScrape()
    hemis = scraped.extractHemispheres()
    latest = scraped.scrapeLatest()
    return  jsonify(latest)

app.run(debug=True)
