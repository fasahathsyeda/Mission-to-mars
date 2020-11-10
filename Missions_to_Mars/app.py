# import necessary libraries(return redirect("http://localhost:5000/", code=302))
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

app.config["MONGO_URI"]="mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#  create route that renders index.html template
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all_content()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return "Scrapping complete. Go back and refresh the page."


if __name__ == "__main__":
    app.run()
