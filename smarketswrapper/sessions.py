import helpers

def connect_session(uname, pw):

    """Function to return a session token given username and password

    Token valid for 30 minutes but extended for 30 minutes if authenticated
    request is sent."""

    data = {'username':uname, "password":pw}

    result = helpers.data_req('sessions/',{'Content-Type':"application/json"}, data)

    if result.status_code==201:
        success = True
        details = result.json()["token"]
    else:
        success = False
        details = "Failed to generate a session token, error type: {0}".format(result.json()['error_type'])
    return success, details

def logout_session()