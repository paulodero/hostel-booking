'''
Created on 4 Oct 2014

@author: podero


This is the webservice that responds to http requests from Google forms' appscript.
'''
import simplejson as json
import ops

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

class RPCMethods:
    def Store(self, params):
        studentName = params['name']
        regNo = params['regNo']
        gender = params['gender']
        programme = params['programme']
        phone_number = params['phone_number']
        disability = params['disability']
        category = params['category']
        emailAddress = params['emailAddress']
        ops.addApplicant(studentName,regNo,gender,programme,phone_number,disability,category,emailAddress)

class RPCHandler(webapp.RequestHandler):
    def __init__(self, request=None, response=None):
        webapp.RequestHandler.__init__(self, request, response)
        self.methods = RPCMethods()
        
    def get(self):
        self.post()  # For debugging purposes, you may want this disabled

    def post(self):
        action = self.request.params['action']
        params = self.request.params['params']
        key = self.request.params['key']

        if not key or key != 'mySecretKey':
            self.error(404) # file not found
            return

        if not action:
            self.error(404) # file not found

        if action[0] == '_':
            self.error(403) # access denied
            return

        func = getattr(self.methods, action, None)

        if not func:
            self.error(404) # file not found
            return

        func(json.loads(params))
        
def main():
    application = webapp.WSGIApplication([('/rpc', RPCHandler)],debug = True)
    util.run_wsgi_app(application)
    
if __name__ == "__main__":
    main()
