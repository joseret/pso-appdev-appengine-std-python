from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class BusinessUser(ndb.Model):
  user_id = ndb.StringProperty(required=True, indexed=True)
  email = ndb.StringProperty(required=True)
