import requests
import datetime
import json

baseurl = "https://api.smarkets.com/v3/"

def data_req(endpoint, headers, data=None, filters=None):

    url = baseurl + endpoint

    if filters is not None:
        formatted_filter = format_filter(filters)
        url+=formatted_filter

    if data is None:
        response = requests.get(url, headers=headers)
    else:
        response = requests.post(url, headers=headers, json=data)

    return response

def order_req(headers, actiontype, params = {}):

    url = baseurl + "orders/"

    if actiontype=="post":
        headers.update({'Content-Type':"application/json"})
        response = requests.post(url, headers=headers, data=json.dumps(params))
    elif actiontype=="get":
        formatted_filter = format_filter(params)
        url += formatted_filter
        response = requests.get(url, headers=headers)

    return response

def format_filter(filters):
    filts = []
    for ky in filters:
        filts.append('&'.join([ky + "={}".format(str(x)) for x in filters[ky]]))
    final_filter = '?' + "&".join(filts)
    return final_filter

def timestamp_todatetime(x):
    x = str(x)[:19]
    x = datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S")
    return x

def datetime_totimestamp(x):
    x = datetime.datetime.strftime(x, "%Y-%m-%dT%H:%M:%SZ")
    return x

def odds_transformer(x):
    return float(x)/10000

def odds_inverter(x):
    return round(float(x)*10000, 0)

def parse_odds_to_df(data):
    contract_ids = list(data.keys())
    df_dict = {"ID": []}
    for i in range(3):
        df_dict['BACK' + str(i)] = []
        df_dict['LAY' + str(i)] = []
        df_dict['BACKSIZE' + str(i)] = []
        df_dict['LAYSIZE' + str(i)] = []

    for competitor in contract_ids:

        lays = data[competitor]['offers']
        backs = data[competitor]['bids']

        df_dict['ID'].append(competitor)

        for i in range(3):
            try:
                back_packet = backs[i]
                px = back_packet['price']
                sz = back_packet['quantity']
            except:
                px = 0
                sz = 0

            df_dict['BACK' + str(i)].append(odds_transformer(px))
            df_dict['BACKSIZE' + str(i)].append(size_transformer(sz, px))

            try:
                lay_packet = lays[i]
                px = lay_packet['price']
                sz = lay_packet['quantity']
            except:
                px = 0
                sz = 0

            df_dict['LAY' + str(i)].append(odds_transformer(px))
            df_dict['LAYSIZE' + str(i)].append(size_transformer(sz, px))

    return pd.DataFrame(df_dict).sort_values(by='BACK1', ascending=False)

def parse_trades_to_df(data):
    df_dict = {}
    contractids = [x['contract_id'] for x in data]
    prices = [float(x['last_executed_price']) / 100 for x in data]
    times = [timestamp_todatetime(x['timestamp']) for x in data]

    df_dict['ID'] = contractids
    df_dict['price'] = prices
    df_dict['timestamp'] = times

    return pd.DataFrame(df_dict).sort_values(by='timestamp', ascending=False)

def size_transformer(sz, px):
    try:
        return (float(sz)*float(px))/100000000
    except:
        return 0

def size_inverter(sz, px):
    return sz*(100000000/float(px))

def size_transformer_series(x):
    sz = x[0]
    px = x[1]
    return round((float(sz) * float(px)) / 100000000, 2)


