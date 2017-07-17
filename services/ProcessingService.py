import os
import logging
import time
import datetime
from google.appengine.ext import ndb



class Simple(ndb.Model):
  customer_type = ndb.StringProperty(required=True)
  business_user = ndb.StringProperty()

class ProcessingService(object):

  def __init__(self, user_info):
    self.__user_info = user_info

  def createCustomerFromJSON(self, customer_info):
    item_business = Simple(key=ndb.Key(Simple, self.__user_info['user_id']), customer_type ="Person", business_user =  str(datetime.datetime.utcnow()))
    item_business.put()


  def getCustomer(self, user_id):
    simple = Simple.get_by_id(user_id)

    return {
      'customerType': simple.customer_type,
      'business_user': simple.business_user,
    }