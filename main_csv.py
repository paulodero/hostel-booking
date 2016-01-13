'''
Created on 9 Jul 2014

@author: podero

This module generated csv files 
'''
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
import ops

urlfetch.set_default_fetch_deadline(20000)

class MainPage(webapp.RequestHandler):   
    def get(self):
        category = self.request.get('category',None) 
        data = ops.getApplicants(category)
        self.response.headers['Content-Type'] = 'text/csv'
        self.response.headers['Content-Disposition'] = "attachment; filename=Applicants.csv"  
        self.response.out.write(','.join(['Name','Registration No.','Gender','Phone No','Programme','disability','Application time']))
    
        for row in data:
            self.response.out.write(','.join(['\n']))
            self.response.out.write(','.join([str(row.studentName),'']))
            self.response.out.write(','.join([str(row.regNo),'']))
            self.response.out.write(','.join([str(row.gender),'']))
            self.response.out.write(','.join([str(row.phone_number),'']))
            self.response.out.write(','.join([str(row.programme),'']))
            self.response.out.write(','.join([str(row.disability),'']))
            self.response.out.write(','.join([str(row.time),'']))
def main():
    application = webapp.WSGIApplication([('/csv', MainPage)], debug=True)
    run_wsgi_app(application)
  
if __name__ == "__main__":
    main()
