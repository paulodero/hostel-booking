'''
Created on Jul 22, 2014

@author: paul

This module contains functions defined in the application
'''
import models
import datetime
import urllib
import urllib2

#Functions to get data from the datastore
#A function to get details of a particular sub-domain sub-domain
def getStudent(reg_no,period):
    q = models.StudentHostel().all().filter('reg_no =', reg_no).filter('period =', period)
    row = q.fetch(1)
    return row

def addApplicant(studentName,regNo,gender,programme,phone_number,disability,category,emailAddress):
    key = regNo
    row = models.HostelApplicants(key_name = key)
    row.studentName = studentName
    row.email = emailAddress
    row.regNo = regNo
    row.gender = gender
    row.programme = programme
    row.phone_number = phone_number
    row.disability = disability
    row.category = category
    row.time = datetime.datetime.now().strftime("%I:%M%p on %B %d  %Y")
    row.active = True
    row.allocated = False
    row.put()
    
def getApplicants(category):
    q = models.HostelApplicants.all().filter('category =', category).filter('active =', True).filter('allocated =', False)
    return q

#A function to get domain from an email address
def getDomainFromEmail(email):
    emailarr = email.split('@')
    subdomain = emailarr[1]
    return subdomain

def isAdmin(email):
    q = models.Admins.all().filter('emailAddress =', email)
    rows = q.fetch(1)
    if rows:
        return True
    return False

def isSuperAdmin(email):
    q = models.Admins.all().filter('emailAddress =', email)
    rows = q.fetch(1)
    if rows:
        return True
    return False

#A function to get domain from a sub-domain
def getDomainFromSubdomain(subdomain):
    emailarr = subdomain.split('.')
    domain = emailarr[1]
    return domain

def addAdmin(email,level):
    key = email
    row = models.Admins(key_name = key)
    row.emailAddress = email
    row.level = '1'
    row.active = True
    row.put()
    
def uploadFile(email,data):
    row = models.uploadedData()
    row.user = email
    row.uploaded = False
    row.data = data
    row.put()
    
def getData():
    q = models.uploadedData.all().filter('uploaded =', False)
    rows = q.fetch(1)
    data = []
    for row in rows:
        row.uploaded = True
        row.put()
        data.append(row)
    return data

def uploadTest(regno,name,gender,hostel,block,roomNo,roomtype,period):
    key = '%s_%s' % (regno.strip(),period)
    row = models.StudentHostel(key_name = key)
    row.reg_no = regno.strip()
    row.name = name
    #row.otherNames = othernames
    row.gender = gender
    row.hostel = hostel
    row.block = block
    row.roomNo = roomNo
    row.roomType = roomtype
    row.period = period
    row.put()
   
#get Periods
def getPeriods():
    q = models.Periods().all()
    row = q.fetch(100)
    return row 

def addPeriod(number,period):
    key = number
    row = models.Periods(key_name = key)
    row.period = period
    row.number = number
    row.put()
    
def verifyUser(email,regno):
    url = 'http://studentmail-ku.appspot.com/rpc'
    regnoArr = regno.split('/')
    if len(regnoArr) > 2:
        reg_no = regnoArr[1] + regnoArr[2]
    else:
        reg_no = regno
    
    params = urllib.urlencode({
                "action": "Echo",
                "params": '{"email":"'+email+'","regno":"'+reg_no+'"}',
                "key": "mySecretKey"
        })
    response = urllib2.urlopen(url, params).read()
    
    if response == '1':
        return True
    else:
        return False
    
def flagApplicant(regno):
    q = models.HostelApplicants().all().filter('regNo =', regno)
    rows = q.fetch(1)
    for row in rows:
        row.active = False
        row.allocated = True
        row.put()  
               
def openApplication():
    q = models.Status().all().filter('number =', '1')
    rows = q.fetch(1)
    for row in rows:
        row.number = '1'
        row.open = True
        row.put()  
    
def allowReApplication():
    q = models.Status().all().filter('number =', '1')
    rows = q.fetch(1)
    for row in rows:
        row.number = '1'
        row.reapplication = True
        row.put()  
            
def disAllowReApp():
    q = models.Status().all().filter('number =', '1')
    rows = q.fetch(1)
    for row in rows:
        row.number = '1'
        row.reapplication = False
        row.put()  
        
def hasApplied(email):
    q = models.HostelApplicants.all().filter('email =', email).filter('active =', True)
    rows = q.fetch(1)
    r = models.Status.all().filter('reapplication =', False)
    reRows = r.fetch(1)
    if rows and reRows:
        return True
    return False

def allocated(email):
    q = models.HostelApplicants.all().filter('email =', email).filter('allocated =', True)
    rows = q.fetch(1)
    if rows:
        return True
    return False

def resetApplications():
    q = models.HostelApplicants().all()
    rows = q.fetch(10000)
    for row in rows:
        row.active = False
        row.allocated = False
        row.put()
        
    q = models.HostelApplicants.all().filter('active =', True)
    rows = q.fetch(1)
    if rows:
        closeApplication()   

def closeApplication():
    q = models.Status().all().filter('number =', '1')
    rows = q.fetch(1)
    for row in rows:
        row.open = False
        row.put()
        
def reAppIsOpen():  
    q = models.Status.all().filter('reapplication =', True)
    rows = q.fetch(1)
    if rows:
        return True
    return False

def applicationOpen():
    q = models.Status.all().filter('open =', True)
    rows = q.fetch(1)
    if rows:
        return True
    return False