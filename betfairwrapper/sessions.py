import requests

def get_sess_token(cert_path, key_path, uname, pw):

    """Returns a session token for future requests using non-interactive login. For details on how to
    get a certificate/key path see https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Non-Interactive+%28bot%29+login

            Parameters:
                cert_path (str): Path to the client certificate on your computer
                key_path (str): Path to the key on your computer
                uname (str): Username for betfair account
                pw (str): Password for betfair account

            Returns:
                success (boolean): True if api call is successful, else false

                details (str):     The session token if successful, else an error message."""

    payload = 'username=' + uname + '&password=' + pw
    headers = {'X-Application': "Key", 'Content-Type': 'application/x-www-form-urlencoded'}

    resp = requests.post('https://identitysso-cert.betfair.com/api/certlogin', data=payload,
                         cert=(cert_path,key_path), headers=headers)

    if resp.status_code == 200:
        loginstatus = resp.json()['loginStatus']
        if loginstatus=="SUCCESS":
            sess_token = resp.json()['sessionToken']
            success = True
            output = sess_token
        else:
            success = False
            output = "Invalid Login details, login status code: {0}".format(loginstatus)
    else:
        success = False
        output = "Unsuccessful request, response code: {0}".format(str(resp.status_code))

    return success, output

def extend_session(session_token, appkey):

    """Submits a request to extend betfair session

            Parameters:
                appkey (str): Betfair Application Key
                sessiontoken (str): Betfair session token

            Returns:
                success (boolean): True if successful and session extended

                details (string): error message if request failed."""

    headers = {'X-Application':appkey, 'Accept':"application/json", "X-Authentication":session_token}
    resp = requests.post("https://identitysso.betfair.com/api/keepAlive", headers=headers)

    if resp.status_code==200:
        success = resp.json()["status"] == "SUCCESS"
        output = resp.json()["error"]
    else:
        success = False
        output = "Request failed, response code: {0}".format(str(resp.status_code))

    return success, output

def logout(session_token, appkey):

    """Returns a dataframe of the Market Types for a given competition id

            Parameters:
                appkey (str): Betfair Application Key
                sessiontoken (str): Betfair session token

            Returns:
                success (boolean): True if request to logout is successful else false

                details (string): error message if request failed."""

    headers = {'X-Application': appkey, 'Accept': "application/json", "X-Authentication": session_token}
    resp = requests.post("https://identitysso.betfair.com/api/logout", headers=headers)

    if resp.status_code==200:
        success = resp.json()["status"] == "SUCCESS"
        output = resp.json()["error"]
    else:
        success = False
        output = "Request failed, response code: {0}".format(str(resp.status_code))

    return success, output







