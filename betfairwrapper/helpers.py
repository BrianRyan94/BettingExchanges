import requests
import datetime

baseurl = "https://api.betfair.com/exchange/betting/json-rpc/v1"


def data_req(appkey, sessiontoken, datatype, params):
    headers = {'X-Application': appkey, 'X-Authentication': sessiontoken, 'content-type': 'application/json'}
    params = format_params(params)
    data = '{"jsonrpc": "2.0", "method":"SportsAPING/v1.0/%s",%s, "id": 1}' % (
        datatype, params)
    data = data.encode('utf-8')
    response = requests.get(baseurl, data=data, headers=headers)
    return response

def timestamp_todatetime(x):
    x = str(x)[:19]
    x = datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S")
    return x

def extract_error(result):
    try:
        error = result.json()['error']['data']['APINGException']['errorCode']
        details = "API exception, error code: {0}".format(error)
    except KeyError:
        error = result.json()['error']['message']
        details = "Response error, message: {0}".format(error)
    return details

def format_params(params):
    if len(params) == 0:
        return '"params": {"filter":{ }}'

    filter = " "
    if 'filter' in params:
        filter = format_filter(params['filter'])
        params_format = '"params": {"filter":{' + filter + '}}'
        del params['filter']

    other_params = []
    for key in params:
        if type(params[key])==list:
            values = '"' + '","'.join([str(x) for x in params[key]]) + '"'
            list_string = "[" + values + "]"
            other_params.append('"{0}":{1}'.format(str(key), list_string))
        elif type(params[key])==dict:
            sub_params = []
            for paramkey in params[key]:
                if type(params[key][paramkey])==list:
                    values = '"' + '","'.join([str(x) for x in params[key][paramkey]]) + '"'
                    list_string = "[" + values + "]"
                    sub_params.append('"{0}":{1}'.format(paramkey, list_string))
                else:
                    sub_params.append('"{0}":"{1}"'.format(str(paramkey), str(params[key][paramkey])))
            param_value = "{" + ",".join(sub_params) + "}"
            other_params.append('"{0}":{1}'.format(str(key),param_value))
        else:
            other_params.append('"{0}":"{1}"'.format(str(key), str(params[key])))

    other_params = ",".join(other_params)
    if other_params=="":
        params_format = '"params": {"filter":{' + filter + '}}'
    else:
        params_format = '"params": {"filter":{' + filter + '},' + other_params + '}'
    return params_format


def format_filter(filters):
    if len(filters) == 0:
        return ""
    else:
        incr = 0
        filter = ""
        for ky in filters:
            filter += "," if incr > 0 else ""
            filter += '"{0}"'.format(ky)
            filter += ":"
            if type(filters[ky]) == list:
                filter += "["
                inc = 0
                for item in filters[ky]:
                    filter += ("" if inc == 0 else ",") + '"{0}"'.format(str(item))
                    inc += 1
                filter += "]"
            else:
                filter += '"{0}"'.format(filters[ky])
            incr += 1
        return filter

def odds_transformer(x):
    if x==0:
        return 0
    else:
        return round(1/x, 4)
