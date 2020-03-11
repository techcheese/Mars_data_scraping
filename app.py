from flask import Flask, render_template, jsonify, request
import scrape_mars 
app = Flask(__name__)

@app.route('/')
def landing():
    scraped = scrape_mars.scrape()
    return jsonify(scraped)

app.run(debug=True)
