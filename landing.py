'''
Created on Jul 19, 2014

@author: paul
'''

import os
import ops

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from settings import TEMPLATES_PATH
from google.appengine.ext.webapp import util
from google.appengine.api import users

DIRECTORY = os.path.dirname(__file__)
_DEBUG = True
values = {}

#Landing Page handler
class LandingPage(webapp.RequestHandler):
    #Render the landing page handler
    def get(self):
        #ops.addPeriod('2015-3','2015-3')
        #ops.flagApplicant('cs282-9398/2331')        
        values =  {}
        user = users.get_current_user()
        values['isSuperAdmin'] = False
        values['isAuthorised'] = False
        values['isLogged'] = False
        values['hasApplied'] = False
        values['statusMessage'] = 'No Reapplication'
        
        if ops.reAppIsOpen():
            values['statusMessage'] = 'Reapplication Open'
        
        if user:
            email = user.email()
            subdomain = ops.getDomainFromEmail(email)
            isAdmin = ops.isAdmin(email)
            isSuperAdmin = ops.isSuperAdmin(email)
            if subdomain != 'ku.ac.ke':
                domain = ops.getDomainFromSubdomain(subdomain)
                if domain != 'ku':
                    self.redirect('/unauthorized')
            values = defaultValues()
            values['isAdmin'] = isAdmin
            values['isSuperAdmin'] = isSuperAdmin
            values['isAuthorised'] = True
            values['isLogged'] = True
            values['hasApplied'] = ops.hasApplied(email)
            
            wireframe = 'home'
        else :
            wireframe = 'unauthorised'
            values =  {}
            values['login_url'] = users.create_login_url('/')
        
        if ops.reAppIsOpen():
            values['statusMessage'] = 'Reapplication Open'
        else:
            values['statusMessage'] = 'No Reapplication'
            
        app_path = os.path.join(DIRECTORY, os.path.join('templates', '%s.html' % wireframe))
        values['app'] = template.render(app_path, values, debug=_DEBUG)
        path = os.path.join(TEMPLATES_PATH,'index.html')
        self.response.out.write(template.render(path, values, debug=_DEBUG))

#Render various application views
class ViewHandler(webapp.RequestHandler):
    def get(self):
        view_info = self.request.path_info.split('/')
        values = defaultValues()
        email = users.get_current_user().email()
        message = ''
        
        
        
            
        if len(view_info)<2:
            return
        view = view_info[1]
        values['isAuthorised'] = True
        
        if view == 'student_details':
            reg_no = self.request.get('regno',None)  
            period = self.request.get('period',None) 
            #Verify Email address and registration number
            email = users.get_current_user().email()
            
            if ops.verifyUser(email, reg_no) or ops.isSuperAdmin(users.get_current_user().email()):
                pass
            else:
                self.redirect('/unauthorized') 
            
            values['student_details'] = ops.getStudent(reg_no,period)
            if len(values['student_details']) > 0:
                wireframe = 'student_details'
            else:
                wireframe = 'record_notfound'                                        
            values['regno'] = reg_no    
                
        elif view == 'application_first':
            if ops.hasApplied(email):
                message = 'You have already applied! You can only apply once!'
                values['message']  = message
                wireframe = 'report'
            elif ops.allocated(email):
                message = 'You have already been allocated hostel! You can not apply again!'
                values['message']  = message
                wireframe = 'report'
            else:
                wireframe = 'application_first'
                
        elif view == 'application_cont':
            if ops.hasApplied(email):
                message = 'You have already applied! You can only apply once!'
                values['message']  = message
                wireframe = 'report'
            elif ops.allocated(email):
                message = 'You have already been allocated hostel! You can not apply again!'
                values['message']  = message
                wireframe = 'report'
            else:
                wireframe = 'application_cont'
                
        elif view == 'status':
            periods = ops.getPeriods()
            values['periods'] = periods
            wireframe = 'status'
            
        elif view == 'unauthorized':
            wireframe = 'unauthorized'
            values['isAuthorised'] = False
            
        elif view == 'openApp':
            ops.openApplication()
            wireframe = 'report'
            message = 'Hostel Applications are Open!'
            
        elif view == 'allowReApp':
            ops.allowReApplication()
            wireframe = 'report'
            message = 'You have allowed hostel Reapplication' 
                     
        elif view == 'disAllowReApp':
            ops.disAllowReApp()
            wireframe = 'report'
            message = 'You have disallowed hostel Re-Application' 
            
        if ops.reAppIsOpen():
            values['statusMessage'] = 'Reapplication Open'
        else:
            values['statusMessage'] = 'No Reapplication'
            
        values['isLogged'] = True  
        values['message']  = message
        values['isSuperAdmin'] = ops.isSuperAdmin(users.get_current_user().email())                   
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
                            'institution': institution
                            
              }      


        
def main():
    application = webapp.WSGIApplication([('/',LandingPage),
                                         ('/.*',ViewHandler)
                                         ],debug = True)
    util.run_wsgi_app(application)
if __name__ == "__main__":
    main()