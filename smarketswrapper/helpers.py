import requests

baseurl = "https://api.smarkets.com/v3/"
def data_req(endpoint, headers, data=None, filter=None):

    url = baseurl + endpoint

    response = requests.post(url, headers=headers, json=data)

    return response