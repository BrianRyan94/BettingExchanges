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



