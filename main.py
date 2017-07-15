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

import os
import logging
import requests
import urllib3
urllib3.disable_warnings()
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


class PrivatePage(webapp2.RequestHandler):
    def get(self):
        # https: // github.com / GoogleCloudPlatform / python - docs - samples / blob / master / appengine / standard / firebase / firenotes / backend / main.py
        print 'Headers', self.request.headers
        value = getAuthHeader('Authorization', self.request.headers)
        print 'Authorization-Header-value', value
        if value:
            id_token = value.split(' ').pop()
            print 'id_token', id_token
            claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST)
            if not claims:
                self.response.status = '401 - Unauthorized'
                return
        else:
            self.response.status = '401 - Unauthorized Missing Header'
            return

        print 'claims', claims

        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<body style=\'background-color: orange\'>Hola, x!</body>')

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<body style=\'background-color: green\'>Hola, Mexico!</body>')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/private', PrivatePage),
], debug=True)