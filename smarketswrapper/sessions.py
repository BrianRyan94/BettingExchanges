import helpers

def connect_session(uname, pw):


    """Returns a session token for authentication of future requests.

                       Parameters:
                           uname (str): username for smarkets account
                           pw (str): password for smarkets account

                       Returns:
                           success (boolean): True if api call is successful, else false

                           details (dictionary/string): If success is true then a dictionary with the bet
                           placement details, otherwise an error. Note that the success field does not necessarily
                           mean the bet is placed - it just means the request and response is all as expected. The
                           response might be that your bet was rejected."""

    data = {'username':uname, "password":pw}

    result = helpers.data_req('sessions/',{'Content-Type':"application/json"}, data)

    if result.status_code==201:
        success = True
        details = result.json()["token"]
    else:
        success = False
        details = "Failed to generate a session token, error type: {0}".format(result.json()['error_type'])
    return success, details

