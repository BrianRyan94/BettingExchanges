import helpers
import pandas as pd

def get_base_events(appkey, sessiontoken):

    """Retrieves a data frame of EventNames:EventIds

    Accepts valid appkey/session token. Return format includes a
    boolean success value and details which is the data frame if success,
    otherwise error details."""

    data_type = "listEventTypes"
    params = {}

    result = helpers.data_req(appkey, sessiontoken, data_type, params)

    if result.status_code==200:

        if 'result' in result.json():
            success = True
            data = result.json()['result']
            eventids = [x['eventType']['id'] for x in data]
            names = [x['eventType']['name'] for x in data]
            details = pd.DataFrame({'Name':names, 'ID':eventids})
        else:
            success = False
            error = result.json()['error']['data']['APINGException'] ['errorCode']
            details = "API exception, error code: {0}".format(error)
    else:
        success = False
        details = "Request for events failed, status code: {0}".format(str(result.status_code))

    return success, details

def get_competitions(appkey, sessiontoken, eventid=None):

    data_type="listCompetitions"

    if eventid is None:
        params = {}
    else:
        params = {'filter':{'eventTypeIds':[eventid]}}

    result = helpers.data_req(appkey, sessiontoken, data_type, params)

    if result.status_code == 200:

        if 'result' in result.json():
            success = True
            data = result.json()['result']
            compids = [x['competition']['id'] for x in data]
            names = [x['competition']['name'] for x in data]
            details = pd.DataFrame({'Name': names, 'ID': compids})
        else:
            success = False
            error = result.json()['error']['data']['APINGException']['errorCode']
            details = "API exception, error code: {0}".format(error)
    else:
        success = False
        details = "Request for competitions failed, status code: {0}".format(str(result.status_code))

    return success, details






