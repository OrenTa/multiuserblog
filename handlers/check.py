import re
from google.appengine.ext import db

def Check(username, password, verify, email, required=True):
    # this list is used to return the results and values for showing in text boxes
    # first two items used for value of username and error text near username
    # and so on for password, verify and email
    # last item is ok/no as a binary true/false (true is ok)
    result = ["", "", "", "", "", "", "", "", "", True]
    result[8] = True

    # check username
    result[0] = username
    if not (username):
        result[1] = "Enter a user name."
        result[8] = False
    else:
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        # checking validity of user name
        if not (USER_RE.match(username)):
            result[1] = "That's not a valid user name."
            result[8] = False
        elif required:
            dbuser = db.GqlQuery("SELECT * FROM User WHERE Name = :n", n=username)
            if dbuser.count()>0:
                result[1] = "User already exists (login or select a new one)."
                result[8] = False

    # check password validity
    result[2] = ""
    USER_RE = re.compile(r"^.{3,20}$")
    # verifing there is a password and that it's ok
    if not (password) or not (USER_RE.match(password)):
        result[3] = "That's not a valid password."
        result[8] = False

    # check verify
    result[4] = ""
    if verify != password:
        result[5] = "Your passwords didn't match."
        result[8] = False

    # check email
    result[6] = email
    USER_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    if email and not (USER_RE.match(email)):
        result[7] = "Your email is not valid."
        result[8] = False

    # see above for the details of result list
    return result
