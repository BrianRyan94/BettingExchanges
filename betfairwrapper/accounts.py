from betfairwrapper import helpers

def get_account_balance(appkey, sessiontoken):

    """Returns dictionary of account details (balance/exposure limit etc).

     Parameters:
                appkey (str): Betfair Application Key
                sessiontoken (str): Betfair session token

            Returns:
                success: True/False indicating if request was successful.

                Details: dictionary/str. Dictionary including account details
                Fields include the available balance, exposure, exposure limit
                and discount rate for the account."""

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