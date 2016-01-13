'''
Created on 19 Oct 2014

@author: podero
'''
'''
Created on 6 Oct 2014

@author: podero
'''
import ops
from google.appengine.ext import webapp

from google.appengine.ext.webapp.util import run_wsgi_app
import os


DIRECTORY = os.path.dirname(__file__)
_DEBUG = True

class MainHandler(webapp.RequestHandler):
    def get(self):
        data = ops.getData()
        register = True
        for dArr in data:
            d = str(dArr.data)
            dataArr = d.split('#')
            count = 0
            for record in dataArr:
                recordArr = record.split(",")
                regno = recordArr[0]
                name =recordArr[1]
                #othernames = recordArr[2]
                gender = recordArr[2]
                hostel = recordArr[3]
                block = recordArr[4]
                roomNo = recordArr[5]
                roomtype = recordArr[6]
                period =  recordArr[7]
                if register and count > 0:
                    ops.addPeriod(period,period)
                    register = False 
                ops.uploadTest(regno,name,gender,hostel,block,roomNo,roomtype,period)
                ops.flagApplicant(regno.strip())
                count = count + 1
                
class ApplicationHandler(webapp.RequestHandler):
    def get(self):
        if ops.applicationOpen():
            ops.resetApplications()
    
def main():
    application = webapp.WSGIApplication([('/cron/update_data', MainHandler),
                                          ('/cron/open_application', ApplicationHandler)], debug=True)
    run_wsgi_app(application)
  
if __name__ == "__main__":
    main()
    