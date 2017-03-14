# Multi User Blog 
https://newblog-161508.appspot.com

This project implements a multi-user blog platform. It enables users to write posts which implements their own blog. Other users can view posts, like them and 
also add comments per post. All actions require to be signed-in to the site while reading/browsing can be done by anyone.
The solution is designed to run on the Google App Engine. 


# Getting Started
### Prerequisits
- setup a personal google account at the google cloud platform (you can use your regular gmail account for that)
- download and install the python Google App Engine SDK from here https://cloud.google.com/appengine/downloads 
- initialize your Google SDK environment as described in the google documentation

### Installing 
- Download/clone this github repository to your local machine

### Running it
- To run it locally go into the folder of the project on your local machine and type dev_appserverp.py . 
- This will start the local SDK server on your machine
- You can then open your browser at http://127.0.0.1:8080/ and start using it

To deploy it follow the google app engine instructions on how to deploy it on your account.

# Built with
- Python 2.7
- Google App Engine SDK
- Python libraries WebApp2 and Jinja (templates)

Note: The project was created as part of the Udacity Full Stack Web Developer nanodegree.


