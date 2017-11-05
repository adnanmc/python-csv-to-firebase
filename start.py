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
    # set id, name, email, age, zip, venue, gender
    self.id = ''
    self.date = ''
    self.fname = ''
    self.lname = ''
    self.email = ''
    self.age = ''
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
            print ('first row, skip this guy')
            writer.writerow(row)
            continue

          # skip this row empty
          if row[2] == '':
            print ('first name was empty')
            writer.writerow(row)
            continue

          # only send one email per instance
          if sentOne == True:
            print ('already sent one - done practicly with csv')
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
          data.id =  str(row[0])
          data.date = str(row[1])
          data.fname = str(row[2])
          data.lname = str(row[3])
          data.email = str(row[4])
          data.birth = str(row[5])
          data.zipcode = str(row[6])
          data.venue = 'theLab'
          data.gender = 'male'
          data.race = 'white'

          # validate birth year
          print('date:')
          print('date: '+data.birth)
          if int(data.birth) < 1900:
            date_object = date.today()
            # get year from date object
            year = date_object.strftime("%Y")
            old = data.birth
            data.birth = int(year)-int(data.birth)
            print('birth year: form >> '+str(old)+' >> '+str(data.birth))

          # ready data for Firebase
          # source: https://stackoverflow.com/questions/10252010/serializing-python-object-instance-to-json
          json = json.dumps(data.__dict__)
          print(json)
          continue

          # if has not been sent, send/push data to Firebase
          # sent = db.child("user").push(data)
          # print ('sent says: '+says)
          # if sent is True:
          #   sentCount += 1
          #   leftToSendCount -=1
          #   row[10] = 'True'
          #   writer.writerow(row)
          #   sentOne = True
          #   continue
          # else:
          #   print('Data did not send: '+email)
          #   errorCount += 1
          #   writer.writerow(row)
          #   continue
    os.rename('data-temp.csv',csvFile)

print('CSV run through and updated.')
print('CSV rows sent: '+str(sentCount))
print('Sending errors: '+str(errorCount))
print('CSV rows left to send: '+str(leftToSendCount))
