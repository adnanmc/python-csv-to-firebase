import pyrebase
from env import config

firebase = pyrebase.initialize_app(config)

# get database
db = firebase.database()

# get data from csv
data = {"name": "Mortimer 'Morty' Smiths"}

# push to firebase
db.child("user").push(data)