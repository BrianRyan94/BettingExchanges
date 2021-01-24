import helpers
import pandas as pd

def get_account_info(sesstoken):

    """Gets account information for a given session

    Returns a dictionary including the account id, available balance,
    balance, bonus balance, commission type, currency and exposure."""

    endpoint = "accounts/"

    headers = {"Authorization": "Session-Token {0}".format(sesstoken)}

    result = helpers.data_req(endpoint, headers)

    if result.status_code==200:
        data = result.json()
        if 'account' in data:
            success = True
            details = data['account']
        else:
            success = False
            details = "Received a response, but no accounts field provided."
    else:
        success = False
        details = "Request for account information failed, status code: {0}".format(str(result.status_code))

    return success, details

def get_account_statement(sesstoken, timeframe=None):

    """Retrieves statement of activity for the account associated
    with the session token provided."""

    endpoint = "accounts/activity/"

    headers = {"Authorization": "Session-Token {0}".format(sesstoken)}

    params = {"limit":["100"], "sort":["-seq%2C-subseq"]}

    if timeframe is not None:
        st_ts = helpers.datetime_totimestamp(timeframe['start'])
        end_ts = helpers.datetime_totimestamp(timeframe['end'])
        params.update({'timestamp_min':[st_ts]})
        params.update({'timestamp_max':[end_ts]})

    result = helpers.data_req(endpoint, headers, filters=params)

    if result.status_code==200:
        data = result.json()
        if 'account_activity' in data:
            success = True
            data = data['account_activity']
            data_dict = {}
            for fld in ['timestamp', 'money','amount', 'commission',
                'event_id','market_id','contract_id','price','order_id']:

                data_dict[fld] = [x.get(fld,"None") for x in data]

            details = pd.DataFrame(data_dict)
            details['timestamp'] = details['timestamp'].apply(helpers.timestamp_todatetime)
            details = details.sort_values(by='timestamp', ascending=False)
        else:
            success = False
            details = "Received response, but no account_activity field found."
    else:
        success = False
        details = "Request for account statement failed, status code: {0}".format(str(result.status_code))

    return success, details








    print(result.json())










