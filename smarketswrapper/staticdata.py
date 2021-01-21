import helpers
import pandas as pd

def get_base_events(sesstoken):

    endpoint = "events/"

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









