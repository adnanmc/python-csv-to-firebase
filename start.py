import pyrebase
from env import config

firebase = pyrebase.initialize_app(config)

# get database
db = firebase.database()

# get data from csv
# loop through csv
data = {"name": "Mortimer 'Morty' Smiths"}

# push to firebase
# db.child("user").push(data)
users = db.child("user").order_by_child("name").equal_to('Jimm').get()

# check if user exists
if users.each():
  print('yep')
else:
  print('nope')

# send data up to firebase