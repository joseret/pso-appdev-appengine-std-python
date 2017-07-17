from google.appengine.ext import ndb

class Contact(ndb.Model):
  phone_number = ndb.StringProperty()
  address = ndb.StringProperty()

