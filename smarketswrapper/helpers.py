import requests

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
