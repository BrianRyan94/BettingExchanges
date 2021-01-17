import helpers

def get_account_balance(appkey, sessiontoken):

    """Returns dictionary of account balance information

    Returns boolean success: True/False, second item returned is a
    dictionary with exposure, exposure limits, available funds to bet,
    and account discount rate if success==True, else an error message."""

    data_type = "getAccountFunds"

    params = {}

    result = helpers.data_req(appkey, sessiontoken, data_type, params, "Account")

    if result.status_code == 200:

        if 'result' in result.json():
            success = True
            data = result.json()['result']
            details ={}
            details = {'AvailableBalance':data['availableToBetBalance'],
                      'Exposure':data['exposure'], 'ExposureLimit':data['exposureLimit'],
                      'Discount':data['discountRate']}
        else:
            success = False
            details = helpers.extract_error(result)
    else:
        success = False
        details = "Request for account balance failed, status code: {0}".format(str(result.status_code))
    return success, details