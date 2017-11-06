from env import config, csvFile
import pyrebase
import csv
import os
import sys, json
from datetime import date

firebase = pyrebase.initialize_app(config)

# get database
db = firebase.database()

# get data from csv
data = {"name": "Mortimer 'Morty' Smiths"}

# vars
sentCount = 0
errorCount = 0
leftToSendCount = 0
sentOne = False

# check if user exists
def doesUserExist(id):
  users = db.child("user").order_by_child(id).equal_to(id).get()
  if users.each():
    return True
  else:
    return False

class PhotoShootDataInstance():
  def __init__(self):
    # set id, name, email, age, zipcode, venue, gender, race
    self._id = ''
    self.date = ''
    self.fname = ''
    self.lname = ''
    self.email = ''
    self.birth = 1900
    self.zipcode = ''
    self.venue = ''
    self.gender = ''
    self.race = ''
    pass

# loop through csv
with open(csvFile) as csv_in_file:
    reader = csv.reader(csv_in_file)
    with open('data-temp.csv', 'w') as csv_out_file:
        writer = csv.writer(csv_out_file)
        # add every preexisting row in CSV before adding another
        for row in reader:
          hasBeenSent = str(row[11])

          # skip first row
          if row[0] == 'id':
            writer.writerow(row)
            continue

          # skip this row empty
          ## ??? there might be a better way to see if row was empty
          ## or how to check if all fields are ready/filled properly
          if row[2] == '':
            writer.writerow(row)
            continue

          # only send one email per instance
          if sentOne == True:
            writer.writerow(row)
            continue

          # don't sent if already sent
          if hasBeenSent == 'True' :
            print ('has been sent')
            writer.writerow(row)
            continue
          else:
            print ('add 1 to left to send var')
            leftToSendCount +=1

          # start data class instance
          data = PhotoShootDataInstance()

          # add data to object
          data._id =  str(row[0])
          data.date = str(row[1])
          data.fname = str(row[2])
          data.lname = str(row[3])
          data.email = str(row[4])
          data.birth = str(row[5])
          data.zipcode = str(row[6])
          data.venue = 'theLab'
          data.event = 'gov conf'
          data.eventLoc = 37738 #gatlinburg by default
          data.gender = 'male'
          data.race = 'white'

          # validate birth year
          if int(data.birth) < 1900:
            date_object = date.today()
            # get year from date object
            year = date_object.strftime("%Y")
            old = data.birth
            data.birth = int(year)-int(data.birth)
            print('birth year: form >> '+str(old)+' >> '+str(data.birth))


          # if has not been sent, send/push data/json to Firebase
          sent = db.child("users").push(data.__dict__)
          ## ??? there might be a better way to measure success
          if isinstance(sent, dict):
            print('is dict')
            # update User Count in Firebase
            usersCount = int(db.child("dashboard").child('usersCount').get())
            db.child("dashboard").update({"usersCount": usersCount})
            sentCount += 1
            leftToSendCount -=1
            row[11] = 'True'
            writer.writerow(row)
            sentOne = True
            continue
          else:
            print('Data did not send (not dict): '+email)
            errorCount += 1
            writer.writerow(row)
            continue
    os.rename('data-temp.csv',csvFile)

print('CSV run through and updated.')
print('CSV rows sent: '+str(sentCount))
print('Sending errors: '+str(errorCount))
print('CSV rows left to send: '+str(leftToSendCount))
