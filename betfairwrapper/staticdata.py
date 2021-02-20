from betfairwrapper import helpers
import pandas as pd

def get_base_events(appkey, sessiontoken):

    """Returns a dataframe of the Market Types for a given competition id

            Parameters:
                appkey (str): Betfair Application Key
                sessiontoken (str): Betfair session token

            Returns:
                success (boolean): True if api call is successful, else false

                details (Dataframe/string): If success is true then a dataframe
                of the event types (2 columns: Event Names/ID)"""

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
            details = helpers.extract_error(result)
    else:
        success = False
        details = "Request for events failed, status code: {0}".format(str(result.status_code))

    return success, details

def get_competitions(appkey, sessiontoken, eventid=None):

    """Returns a dataframe of the Market Types for a given competition id

            Parameters:
                appkey (str): Betfair Application Key
                sessiontoken (str): Betfair session token
                eventid *optional* (str/int): Event ID (e.g. Golf: 3) for which you want competitions

            Returns:
                success (boolean): True if api call is successful, else false

                details (Dataframe/string): If success is true then a dataframe
                of the competitions (2 columns: Name/ID)"""

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
            details = helpers.extract_error(result)
    else:
        success = False
        details = "Request for competitions failed, status code: {0}".format(str(result.status_code))

    return success, details

def get_mkt_types_for_comp(appkey, sessiontoken, competitionid):

    """Returns a dataframe of the Market Types for a given competition id

            Parameters:
                appkey (str): Betfair Application Key
                sessiontoken (str): Betfair session token
                tournamentid (str/int): Tournament ID (e.g. Premier League: 3) for which you want time range

            Returns:
                success (boolean): True if api call is successful, else false

                details (Dataframe/string): If success is true then a dataframe
                of the market types (1 column: Market Types)"""

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
            details = helpers.extract_error(result)
    else:
        success = False
        details = "Request for market types failed, status code: {0}".format(str(result.status_code))

    return success, details

def get_timerange_competition(appkey, sessiontoken, competitionid, granularity="DAYS"):

    """Returns a dataframe of the time ranges for a given competition id

            Parameters:
                appkey (str): Betfair Application Key
                sessiontoken (str): Betfair session token
                tournamentid (str/int): Tournament ID (e.g. Premier League: 3) for which you want time range

            Returns:
                success (boolean): True if api call is successful, else false

                details (Dataframe/string): If success is true then a dataframe
                of the competition time ranges (1 row: columns start/end) """

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
            details = helpers.extract_error(result)
    else:
        success = False
        details = "Request for time ranges failed, status code: {0}".format(str(result.status_code))

    return success, details


def get_runner_names(appkey, sessiontoken, marketid):

    """Returns competitor/runner names in dataframe form for a given market

        Parameters:
            appkey (str): Betfair Application Key
            sessiontoken (str): Betfair session token
            marketid (str/int): Market ID (e.g. Pga Championship: Winner) for which you want competitors

        Returns:
            success (boolean): True if api call is successful, else false

            details (Dataframe/string): If success is true then a dataframe
            of the runners with runner name/runner id as the columns"""

    data_type = "listMarketCatalogue"

    params = {"filter":{"marketIds":[marketid]},"maxResults":"1000", "marketProjection":["RUNNER_DESCRIPTION"]}

    result = helpers.data_req(appkey, sessiontoken, data_type, params)

    if result.status_code == 200:
        if 'result' in result.json():

            try:
                data = result.json()['result'][0]['runners']
            except IndexError:
                return False, "No runner data was found for market ID: {0}".format(marketid)
            except ValueError:
                return False, "No runner data was found for market ID: {0}".format(marketid)

            success = True
            selectionids = [x['selectionId'] for x in data]
            runnernames = [x['runnerName'] for x in data]
            details = pd.DataFrame({'Name': runnernames, "ID": selectionids})
        else:
            success = False
            details = helpers.extract_error(result)

    else:
        success = False
        details = "Request for time runner names failed, status code: {0}".format(str(result.status_code))

    return success, details

def get_market_catalogue(appkey, sessiontoken, tournamentid=None, matchid=None):

    """Returns a market catalogue in dataframe form given filters on tournaments/matches

        Parameters:
            appkey (str): Betfair Application Key
            sessiontoken (str): Betfair session token
            tournamentid *optional* (str/int): Tournament ID (e.g. Premier League: 3) for which you want markets returned
            matchid *optional* (str/int): Match ID (e.g. Man Utd Vs Arsenal) for which you want markets returned

        Returns:
            success (boolean): True if api call is successful, else false

            details (Dataframe/string): If success is true then a dataframe
            of the markets including the marketid/marketname and total matched.
            If success==false, a string detailing the error."""

    data_type = "listMarketCatalogue"

    params = {'maxResults':"100"}

    filter = {}

    if tournamentid is not None:
        filter.update({"competitionIds": [str(tournamentid)]})

    if matchid is not None:
        filter.update({"eventIds": [str(matchid)]})

    if len(filter)!=0:
        params.update({"filter":filter})

    result = helpers.data_req(appkey, sessiontoken, data_type, params)

    if result.status_code==200:
        if 'result' in result.json() and len(result.json()['result'])>0:
            data = result.json()['result']
            success = True
            data_dict = {}

            for fld in ['marketId', 'marketName','totalMatched']:
                data_dict[fld] = [x[fld] for x in data]

            details = pd.DataFrame(data_dict)
        else:
            success = False
            try:
                details = helpers.extract_error(result)
            except:
                details = "Received response, but no markets found for tournament ID: {0}, match ID".format(tournamentid, matchid)
    else:
        success = False
        details = "Request for market catalogue failed, status code: {0}".format(str(result.status_code))

    return success,details

def get_matches(appkey, sessiontoken, tournamentid=None, eventid=None, timeframe=None):

    """Returns matches (referred to as events) from Betfair

    Parameters:
        appkey (str): Betfair Application Key
        sessiontoken (str): Betfair session token
        tournamentid (str/int): Tournament ID (e.g. Premier League: 3) for which you want matches returned
        eventid (str/int): Event Type ID (e.g. 7 for Horse Racing)
        timeframe dict: Dictionary taking two keys: start, end and datetime values for both.

    Returns:
        success (boolean): True if api call is successful, else false

        details (Dataframe/string): If success is true then a dataframe
        of the matches including the name/matchid/timezone and opendate.
        If false, a string detailing the error."""

    data_type = "listEvents"
    filter = {}
    params = {}

    if eventid!=None:
        filter.update({"eventTypeIds":[str(eventid)]})
    if tournamentid!=None:
        filter.update({"competitionIds": [str(tournamentid)]})
    if timeframe!=None:
        filter.update({"marketStartTime":{"from":helpers.datetime_totimestamp(timeframe["start"]),\
                                          "to":helpers.datetime_totimestamp(timeframe["end"])}})

    params.update({"filter":filter})

    result = helpers.data_req(appkey, sessiontoken, data_type, params)

    if result.status_code==200:
        data = result.json()
        if 'result' in data:
            success = True
            data = data['result']
            data = [x['event'] for x in data]

            data_dict = {}
            for fld in ['name', 'id', 'timezone', 'openDate']:
                data_dict[fld] = [x[fld] for x in data]
            details = pd.DataFrame(data_dict)
            details = details.rename(columns={'name':'MatchName', 'id':'MatchID'})
        else:
            success = False
            try:
                details = helpers.extract_error(result)
            except:
                details = "Response code 200 received, but no results field in body."
    else:
        success = False
        details = "Request for matches failed, status code: {0}".format(str(result.status_code))

    return success, details




















