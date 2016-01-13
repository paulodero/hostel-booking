# hostel-booking
student hostel booking and allocation

An application that integrates google docs and google appengine to help educational institutions in hostel booking and allocation.

It has web service which receives data populated from google forms. The google forms sends data to the appengne web service using google appscript http request.

Data is uploaded into google appengine inform of csv and stored as text in the datastore which is then processed by a cron job.

The application ensures student information is confidential by utilising google appengine authentication mechanisms.

Application already in use by a number of universities in kenya.
