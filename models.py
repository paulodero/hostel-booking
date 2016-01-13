'''
Created on Jul 22, 2014

@author: paul

This module defines the datastore structure
'''

from google.appengine.ext import db

#Information structure of registered domains' entities
class Student(db.Model):
    emailAddress = db.StringProperty()
    firstName = db.StringProperty()
    lastName = db.StringProperty()
    password = db.StringProperty()

class StudentHostel(db.Model):
    reg_no = db.StringProperty()
    name = db.StringProperty()
    #otherNames = db.StringProperty()
    gender = db.StringProperty()
    hostel = db.StringProperty()
    block = db.StringProperty()
    roomNo = db.StringProperty()
    roomType =db.StringProperty()
    ''' period is defined in the following format
    year-semester e.g 2014-1,2014-2,2014-3'''
    period = db.StringProperty()
    
class HostelApplicants(db.Model):
    studentName = db.StringProperty()
    regNo = db.StringProperty()
    gender = db.StringProperty()
    email = db.StringProperty()
    programme = db.StringProperty()
    phone_number = db.StringProperty()
    disability = db.StringProperty()
    """Categories:
    1. First year
    2. Continuing """
    category = db.StringProperty()
    time = db.StringProperty()
    active = db.BooleanProperty()
    allocated = db.BooleanProperty()
    
class Admins(db.Model):
    emailAddress = db.StringProperty()
    level = db.StringProperty()
    active = db.BooleanProperty()
    
class uploadedData(db.Model):
    user = db.StringProperty()
    uploaded = db.BooleanProperty()
    data = db.TextProperty()
    
class TestData(db.Model):
    regno = db.TextProperty()
    surname = db.StringProperty()
    othernames = db.StringProperty()
    gender = db.StringProperty()
    hostel = db.StringProperty()
    roomtype = db.StringProperty()
    
class Periods(db.Model):
    number = db.StringProperty()
    period = db.StringProperty()

class Status(db.Model):
    number = db.StringProperty()
    open = db.BooleanProperty()
    reapplication = db.BooleanProperty()