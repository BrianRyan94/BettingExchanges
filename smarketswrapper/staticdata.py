from smarketswrapper import helpers
import pandas as pd

def get_base_events(sesstoken):


    """Returns a dataframe of the base events (golf/tennis etc).

                       Parameters:
                           sessiontoken (str): Smarkets session token

                       Returns:
                           success (boolean): True if api call is successful, else false

                           details (dataframe/string): If success is true then a dataframe with the
                           base event details including the event names/event ids. If success==false,
                           an error message"""

    endpoint = "events/?limit=100"

    headers = {"Authorization": "Session-Token {0}".format(sesstoken)}

    result = helpers.data_req(endpoint, headers)

    if result.status_code==200:
        if 'events' in result.json():
            success = True
            data = result.json()['events']
            names = [x['name']  for x in data]
            ids = [x['id'] for x in data]
            details = pd.DataFrame({'Name':names, 'ID':ids})
        else:
            success = False
            details = "Response code 200, but no events retrieved."
    else:
        success = False
        details = "Request for events failed, status code: {0}".format(str(result.status_code))

    return success, details

def get_child_events(sesstoken, parentid, extra_filters = {}):


    """Returns a dataframe of the child events of a given parent event.

    E.g. pass the golf event id as the parent id and it will return golf tournaments
    Pass the pga championship event id and it will return all markets for that tournament.

                       Parameters:
                           sessiontoken (str): Smarkets session token
                           parentid (str/int): parent id for which you want child events returned
                           extra_filters (dict): Any key:value pairs you want to pass as filters.
                           Check https://docs.smarkets.com/#/orders/create_order for the schema.

                       Returns:
                           success (boolean): True if api call is successful, else false

                           details (dataframe/string): If success is true then a dataframe of the
                           child events including the name, id, created date, state, start date,
                           start date time, and whether the event is bettable (are you at a leaf in
                           the tree)."""

    endpoint = "events/"

    headers = {"Authorization": "Session-Token {0}".format(sesstoken)}

    filt = {'parent_id': [parentid]}

    for filtr in extra_filters:
        filt.update({filtr:extra_filters[filtr]})

    result = helpers.data_req(endpoint, headers, filters=filt)

    if result.status_code == 200:
        if 'events' in result.json():
            success = True
            data = result.json()['events']
            names = [x['name'] for x in data]
            ids = [x['id'] for x in data]
            created = []
            for x in data:
                try:
                    created.append(helpers.timestamp_todatetime(x['created']))
                except:
                    created.append(str(x['created']))
            state = [x['state'] for x in data]
            start_date = [x['start_date'] for x in data]
            start_datetime = [x['start_datetime'] for x in data]
            bettable = [x['bettable'] for x in data]

            details = pd.DataFrame({'Name': names, 'ID': ids, 'created':created,
                                    'state':state, 'start_date':start_date,'start_datetime':start_datetime,
                                    'bettable':bettable})
        else:
            success = False
            details = "Response code 200, but no events retrieved."
    else:
        success = False
        details = "Request for events failed, status code: {0}".format(str(result.status_code))

    return success,details

def get_market_types(sesstoken, bettable_id):

    """Returns a dataframe of market types for a bettable event.

                       Parameters:
                           sesstoken (str): Smarkets session token
                           bettable_id(str/int): The bettable event ID for which you want the market types.

                       Returns:
                           success (boolean): True if api call is successful, else false

                           details (dataframe/string): If success is true then a dataframe of the
                           market names/ids and other metadata associated with each market.
                           If success==false, an error string."""

    endpoint = "events/{0}/markets?sort=event_id%2Cdisplay_order".format(str(bettable_id))

    headers = {"Authorization": "Session-Token {0}".format(sesstoken)}

    result = helpers.data_req(endpoint, headers)

    if result.status_code == 200:
        data = result.json()
        if 'markets' in data and len(data['markets'])>0:
            success = True

            data = data['markets']
            df_dict = {}
            for field in ['name', 'id', 'bet_delay', 'cashout_enabled', 'inplay_enabled', 'state', 'winner_count']:
                df_dict[field] = [x[field] for x in data]

            details = pd.DataFrame(df_dict)
        else:
            success = False
            details = "Reponse code 200, but no markets retrieved."
    else:
        success = False
        details = "Request for market types failed, status code: {0}".format(str(result.status_code))

    return success, details

def get_contracts_for_market(sesstoken, marketid):

    """Returns a dataframe of contracts associated with a marketid.

    *By contracts I mean "choices". For example if the market ID passed is
    for the "Winner" market of a football game the contracts will be the 2 teams.

                           Parameters:
                               sesstoken (str): Smarkets session token
                               marketid(str/int): The market ID for which you want the contracts returned.

                           Returns:
                               success (boolean): True if api call is successful, else false

                               details (dataframe/string): If success is true then a dataframe of the
                               contracts (the names/ids/state). If success==false, an error string."""

    endpoint = "markets/{0}/contracts/".format(str(marketid))

    headers = {"Authorization": "Session-Token {0}".format(sesstoken)}

    result = helpers.data_req(endpoint, headers)

    if result.status_code==200:
        data = result.json()
        if 'contracts' in data and len(data['contracts'])>0:
            success = True
            data = data['contracts']
            df_dict = {}

            for colname in ['name', 'competitor_id', 'id','state_or_outcome']:
                df_dict[colname] = [x[colname] for x in data]
            details = pd.DataFrame(df_dict)
        else:
            success = False
            details = "Response received but not contracts found for market id {0}".format(marketid)
    else:
        success = False
        details = "Request for contracts failed, status code: {0}".format(str(result.status_code))

    return success, details









