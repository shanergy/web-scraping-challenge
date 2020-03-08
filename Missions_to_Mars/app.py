#**************************************************************************************************#
# Import Dependencies
#**************************************************************************************************#
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish a MongoDB connection
mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_data_app')


#**************************************************************************************************#
# Route to render index.html template using MongoDB
#**************************************************************************************************#
@app.route('/')
def home():
    # Find a record of data from MongoDB
    mars_data = mongo.db.collection.find_one()

    # Return template & data
    return render_template('index.html', mars_data=mars_data)


#**************************************************************************************************#
# Route that triggers scrape function
#**************************************************************************************************#
@app.route('/scrape')
def scrape():
    # Run scrape function
    mars_data = scrape_mars.scrape()

    # Update MongoDB using update & upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect to Home Page
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)