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
