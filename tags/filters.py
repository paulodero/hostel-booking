'''
Created on Oct 15, 2012

@author: paul
'''
from google.appengine.ext import webapp

register = webapp.template.create_template_register()
#Remove spaces in a string
def removeSpacesInString(thestrings):
    thestringsarr = thestrings.split()
    string = ''
    for thestring in thestringsarr:
        string += thestring
    return string

register.filter(removeSpacesInString)
