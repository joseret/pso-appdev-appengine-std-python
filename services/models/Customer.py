from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
from google.appengine.ext.ndb import msgprop

class Customer(ndb.Model):
  customer_type = ndb.StringProperty(required=True)
  business_user = ndb.StringProperty()
