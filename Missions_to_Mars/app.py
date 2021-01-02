from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.Mars
collection = db.collection

# Create an instance of Flask
app = Flask(__name__)



# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    planet_data = collection.find_one()

    # Return template and data
    return render_template("index.html", data=planet_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function"
    mars_data = scrape_mars.scrape()
    print("#scrape function ran")

    # Update the Mongo database using update and upsert=True
    collection.update({}, mars_data, upsert=True)
    print("#database update completed")
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)


#%%
mongo.Mars.collection.update({}, mars_data, upsert=True)
