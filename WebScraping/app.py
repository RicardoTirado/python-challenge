# Import dependencies
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)

# Root URL that gets data from MongoDB
@app.route("/")
def index():
    mars = mongo.db.marsDB.find_one()
    return render_template("index.html", mars=mars)

# Scrape data using scrape_mars.py file, then update MongoDB database
@app.route("/scrape")
def scraper():
    mars = mongo.db.marsDB
    # Store scraped data in mars_data dict
    mars_data = scrape_mars.scrape()
    # Store the dict data into MongoDB
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    # Route the browser back to root directory
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)