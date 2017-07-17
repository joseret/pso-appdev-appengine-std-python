# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import logging
import requests
import urllib3
urllib3.disable_warnings()
from urlparse import urlparse
import webapp2

import google
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
  # Production, no need to alter anything
  pass
else:
  # Local development server
  google.__path__.pop(0)  # remove /home/<username>/.local/lib/python2.7/site-packages/google
  logging.warning(google.__path__)  # to inspect the final __path__ of module google

logging.warn(os.path.dirname(google.__file__))
google.__path__.append('./lib/google')

import google.oauth2.id_token
import google.auth.transport.requests

import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()
HTTP_REQUEST = google.auth.transport.requests.Request()


import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth as firebase_auth


if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
  # Production, no need to alter anything
  try:
    default_app = firebase_admin.get_app()
  except:
    default_app = firebase_admin.initialize_app()
else:
  # Local development server
  cred = credentials.Certificate('localonly/pso-appdev-gnp-mex-firebase-adminsdk-fhph7-a3ddb7abd2.json')
  try:
    default_app = firebase_admin.get_app()
  except:
    default_app = firebase_admin.initialize_app(cred)
# Initialize the app with a service account, granting admin privileges

from services.ProcessingService import ProcessingService


def getAuthHeader(key, headers):
    print 'getAuthHeader', headers.items()
    try:
        for header in headers.items():
            print 'header', header, len(header)
            if len(header) > 1:
              if header[0] == key:
                return header[1]
        print 'getAuthHeader', None
    except:
        return None
    return None

def getAuthInfo(request):
  print 'Headers', request.headers
  value = getAuthHeader('Authorization', request.headers)
  print 'Authorization-Header-value', value
  if value:
    id_token = value.split(' ').pop()
    print 'id_token', id_token
    claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST)
    if not claims:
      return {'auth': False, 'info': id_token, 'step': 'claims'}

    decoded_token = firebase_auth.verify_id_token(id_token)
    if not decoded_token:
      return {'auth': False, 'info': id_token, 'step': 'firebase_decoded'}

    return { 'auth' : True, 'info': decoded_token, 'step': 'success'}
  else:
    return { 'auth' : False, 'info': None}


class RestHandler(webapp2.RequestHandler):
  def post(self):
    logging.info("RestHandler-start-url[{0}]".format(self.request.url))
    result = getAuthInfo(self.request)
    if not 'auth' in result:
      logging.error("Auth Check not returning appropriate dict - key = auth")
      self.response.status = '500 - Unexpected Error'
      return
    if not result['auth']:
      logging.warning("Auth Check for token failed - [{0}]". str(result))
      self.response.status = '401 - Unauthorized Error'
      return

    print '-----------result--------------', result
    parsedUrl = urlparse(self.request.url)
    json_data = json.loads(self.request.body)
    ps = ProcessingService({'user_id': str(result['info']['uid']), 'email': unicode(result['info']['email'])})
    if parsedUrl.path == '/rest/customer':

      ps.createCustomerFromJSON(json_data)
      customer_info = ps.getCustomer(str(result['info']['uid']))
      self.response.headers['Content-Type'] = 'text/json'
      self.response.write(json.dumps(customer_info))


class PrivatePage(webapp2.RequestHandler):
    def get(self):
        # https: // github.com / GoogleCloudPlatform / python - docs - samples / blob / master / appengine / standard / firebase / firenotes / backend / main.py

        value = getAuthHeader('Authorization', self.request.headers)
        print 'Authorization-Header-value', value
        if value:
            id_token = value.split(' ').pop()
            print 'id_token', id_token
            claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST)

            if not claims:
                self.response.status = '401 - Unauthorized'
                return
            decoded_token = firebase_auth.verify_id_token(id_token)
            if not decoded_token:
                self.response.status = '401 - Unauthorized - Firebase'
                return
        else:
            self.response.status = '401 - Unauthorized Missing Header'
            return

        print 'claims', claims
        print 'decoded_token', decoded_token
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<body style=\'background-color: orange\'>Hola, x!</body>')

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<body style=\'background-color: green\'>Hola, Mexico!</body>')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/private', PrivatePage),
    ('/rest/customer', RestHandler),
], debug=True)