import requests

def get_sess_token(cert_path, key_path, uname, pw):
    """Returns a session token for non-interactive logins

    To setup a certificate to allow you to do this visit
    https://docs.developer.betfair.com/pages/viewpage.action?pageId=3834909#Login&SessionManagement-Non-Interactivelogin
    Must pass the path to this certificate, path to the key, application key, username and password to retrieve the session token"""

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

    """Submits a request to betfair to extend the session

    Accepts the session token and application key as inputs. Returns boolean value indicating
    whether the session was successfully extended, and a text output with further details of failed
    requests"""

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

    """Attempts to logout of the session

    Accepts session token and app key. Returns boolean success and
    extra details for failed requests"""

    headers = {'X-Application': appkey, 'Accept': "application/json", "X-Authentication": session_token}
    resp = requests.post("https://identitysso.betfair.com/api/logout", headers=headers)

    if resp.status_code==200:
        success = resp.json()["status"] == "SUCCESS"
        output = resp.json()["error"]
    else:
        success = False
        output = "Request failed, response code: {0}".format(str(resp.status_code))

    return success, output







