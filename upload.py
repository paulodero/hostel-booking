'''
Created on 6 Oct 2014

@author: podero
'''

import cgi
import ops
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from settings import TEMPLATES_PATH
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import os

DIRECTORY = os.path.dirname(__file__)
_DEBUG = True

class MainHandler(webapp.RequestHandler):
    def get(self):
        values = defaultValues()
        wireframe = 'upload_csv'
                    
        values['isAuthorised'] = True
        values['isLogged'] = True    
        values['isSuperAdmin'] = ops.isSuperAdmin(users.get_current_user().email())   
        app_path = os.path.join(TEMPLATES_PATH,'%s.html' % wireframe)
        values['app'] = template.render(app_path, values, debug=_DEBUG)
        path = os.path.join(TEMPLATES_PATH,'index.html')
        self.response.out.write(template.render(path, values, debug=_DEBUG))
        

class UploadHandler(webapp.RequestHandler):
    def post(self):  
        user = users.get_current_user() 
        email = user.email()     
        form = cgi.FieldStorage()
        filedata = form['hostupload']
        data = filedata.value
        ops.uploadFile(email, data)
        values = defaultValues()
        wireframe = 'upload_csv'                   
        values['isAuthorised'] = True
        values['isLogged'] = True    
        values['isSuperAdmin'] = ops.isSuperAdmin(users.get_current_user().email())   
        values['upload_message'] = 'File uploaded and will be processed in not more than 10 mins!'
        app_path = os.path.join(TEMPLATES_PATH,'%s.html' % wireframe)
        values['app'] = template.render(app_path, values, debug=_DEBUG)
        path = os.path.join(TEMPLATES_PATH,'index.html')
        self.response.out.write(template.render(path, values, debug=_DEBUG))

def defaultValues():
    user = users.get_current_user()
    nickname = user.nickname()
    logout_url = users.create_logout_url('/')
    institution = "Kenyatta University"
    return  {
               'owner': nickname,
               'email': user.email(),
               'logout_url': logout_url,
               'owner': user.email(),
              'institution': institution,
              'upload_message':''
            }      
def main():
    application = webapp.WSGIApplication([('/upload_csv', MainHandler),
                               ('/upload', UploadHandler)], debug=True)
    run_wsgi_app(application)
  
if __name__ == "__main__":
    main()
    