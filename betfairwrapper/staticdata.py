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

    """Retrieves a data frame of competitions for an event (i.e. Golf)

    Dataframe has the tournament name and ID. Returns 2 values - a boolean
    indicating whether the retrieval was successful, and details (the dataframe
    if successful and an error message otherwise."""

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

def get_mkt_types_for_comp(appkey, sessiontoken, competitionid):

    """Retrieves a dataframe of the market types available for a given competition id.

    Returns a boolean success value, and a details value containing the result if successful
    otherwise an error message."""

    data_type="listMarketTypes"

    params = {'filter':{'competitionIds':[competitionid]}}

    result = helpers.data_req(appkey, sessiontoken, data_type, params)

    if result.status_code == 200:

        if 'result' in result.json():
            success = True
            data = result.json()['result']
            markettypes = [x['marketType'] for x in data]
            details = pd.DataFrame({'MarketType':markettypes})
        else:
            success = False
            error = result.json()['error']['data']['APINGException']['errorCode']
            details = "API exception, error code: {0}".format(error)
    else:
        success = False
        details = "Request for market types failed, status code: {0}".format(str(result.status_code))

    return success, details

def get_timerange_competition(appkey, sessiontoken, competitionid, granularity="DAYS"):

    """Retrieves a dataframe of the time ranges for a given competition id.

    Returns a boolean success value, and a details value containing the result if successful
    otherwise an error message. It can return multiple values if there are multiple markets
    with different start and end times matching the competitionID filter based on the granularity"""

    data_type="listTimeRanges"

    params = {'filter':{'competitionIds':[competitionid]},"granularity":granularity}

    result = helpers.data_req(appkey, sessiontoken, data_type, params)

    if result.status_code == 200:

        if 'result' in result.json():
            success = True
            data = result.json()['result']
            time_from = [helpers.timestamp_todatetime(x['timeRange']['from']) for x in data]
            time_to = [helpers.timestamp_todatetime(x['timeRange']['to']) for x in data]
            details = pd.DataFrame({'Start':time_from, "End":time_to})
        else:
            success = False
            error = result.json()['error']['data']['APINGException']['errorCode']
            details = "API exception, error code: {0}".format(error)
    else:
        success = False
        details = "Request for time ranges failed, status code: {0}".format(str(result.status_code))

    return success, details







