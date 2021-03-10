import pandas as pd
from betfairwrapper import helpers

def list_orders(appkey, sessiontoken, since=None, until=None):
    """Returns a dictionary of dataframes corresponding to filled/live and cancelled orders.

            Parameters:
                appkey (str): Betfair Application Key
                sessiontoken (str): Betfair session token
                since *optional* (datetime): Filter for orders from time created
                until *optional* (datetime): Filter for orders before time created

            Returns:
                success (boolean): True if api call is successful, else false

                details (dictionary/string): If success is true then a dictionary with
                3 dataframes. Dictionary keys are live (dataframe of live orders),
                fills (dataframe of filled orders) and cancelled (dataframe of cancelled
                orders). If the request failed, returns an error."""

    data_type = "listCurrentOrders"

    params = {"dateRange": {}}

    if since != None:
        since = helpers.datetime_totimestamp(since)
        until = helpers.datetime_totimestamp(until)
        params["dateRange"].update({"from": since})
        params["dateRange"].update({"to": until})

    result = helpers.data_req(appkey, sessiontoken, data_type, params)

    if result.status_code == 200:

        def try_convert_odds(x):
            try:
                return helpers.odds_transformer(float(x))
            except:
                return x

        def try_convert_timestamp(x):
            try:
                return helpers.timestamp_todatetime(x)
            except:
                return x

        if 'result' in result.json():
            success = True
            data = result.json()['result']['currentOrders']
            df_dict = {}
            for fld in ["betId", "marketId", "selectionId", "side", "status",
                        "orderType", "placedDate", "matchedDate", "averagePriceMatched",
                        "sizeMatched", "sizeCancelled", "sizeVoided", "sizeRemaining"]:
                df_dict[fld] = [x.get(fld, "NotFound") for x in data]

            df_dict["price"] = [x.get("priceSize", {}).get("price", "NotFound") for x in data]
            df_dict["size"] = [x.get("priceSize", {}).get("size", "NotFound") for x in data]

            details = pd.DataFrame(df_dict)

            details['averagePriceMatched'] = details['averagePriceMatched'].apply(lambda x: try_convert_odds(x))
            details['price'] = details['price'].apply(lambda x: try_convert_odds(x))

            details['placedDate'] = details['placedDate'].apply(try_convert_timestamp)
            details['matchedDate'] = details['matchedDate'].apply(try_convert_timestamp)


            live = helpers.extract_order_type(details, 'live')
            fills = helpers.extract_order_type(details, 'fills')
            cancelled = helpers.extract_order_type(details, 'cancelled')

            details = {'live':live, 'fills':fills, 'cancelled':cancelled}

        else:
            success = False
            details = helpers.extract_error(result)
    else:
        success = False
        details = "Request for order details failed, status code: {0}".format(str(result.status_code))

    return success, details


def placeOrder(appkey, sessiontoken, marketid, selectionid, side, amount, limitprob):

    """Places a limit order with order type LAPSE (lapse the order when market goes in play).

                Parameters:
                    appkey (str): Betfair Application Key
                    sessiontoken (str): Betfair session token
                    marketid (str/int): Market ID for order
                    selectionid (str/int): Selection ID for order
                    side (BACK/LAY): Side for order
                    amount: Amount in account currency to bet
                    limitprob (float): The probability you are buying/selling (e.g. 0.05 if you are buying 20.0)

                Returns:
                    success (boolean): True if bet placement is successful, else false

                    details (Dataframe/string): If success is true then a dataframe with bet details
                    including betid/placeddate/status/size matched/average price matched."""

    limitpx = round(helpers.odds_inverter(limitprob),1)

    data_type = "placeOrders"

    instructions = [{"selectionId": selectionid, "handicap": 0,
                     "side": side, "orderType": "LIMIT",
                     "limitOrder": {"size": amount, "price": limitpx,
                                    "persistenceType": "LAPSE"}
                     }]

    params = {"marketId": marketid,
              "instructions": instructions}

    result = helpers.data_req(appkey, sessiontoken, data_type, params)

    if result.status_code == 200:
        data = result.json()
        if 'result' in data:
            if 'status' in data['result']:
                if data['result']['status'] == "SUCCESS":
                    success = True
                    betid = data['result']['instructionReports'][0]['betId']
                    placeddate = helpers.timestamp_todatetime(data['result']['instructionReports'][0]['placedDate'])
                    orderstatus = data['result']['instructionReports'][0]['orderStatus']
                    pxmatched = data['result']['instructionReports'][0]['averagePriceMatched']
                    sizematched = data['result']['instructionReports'][0]['sizeMatched']
                    details = pd.DataFrame({'betId': [betid], 'placedDate': [placeddate],
                                            'orderStatus': [orderstatus], 'averagePriceMatched': [pxmatched],
                                            'sizeMatched': [sizematched]})

                else:
                    success = False
                    status = data['result']['status']
                    details = "Bet placement failed, received the following json response: {0}".format(str(data['result']))
            else:
                success = False
                details = "Bet placement failed, no status sent back in response"
        else:
            success = False
            details = "Failed to place bet, error details: {0}".format(str(data))

    return success, details

def cancelOrder(appkey, sessiontoken, marketid, betid, sizereduction=None):

    """Cancel/reduce the size of a live bet.

                    Parameters:
                        appkey (str): Betfair Application Key
                        sessiontoken (str): Betfair session token
                        marketid (str/int): Market ID for order
                        betid (str/int): Bet ID for cancellation
                        sidereduction (float): Amount in account currency you want to reduce the bet

                    Returns:
                        success (boolean): True if bet cancellation is successful, else false

                        details (Dataframe/string): If success is true then a dataframe with cancellation
                        details including the bet id, size cancelled, and cancelled time. If false,
                        an error message."""

    data_type = "cancelOrders"

    if sizereduction==None:
        instructions = [{"betId": betid}]
    else:
        instructions = [{"betId":betid, "sizeReduction":sizereduction}]

    params = {'marketId':marketid,"instructions":instructions}

    result = helpers.data_req(appkey, sessiontoken, data_type, params)

    if result.status_code == 200:
        data = result.json()
        if 'result' in data:
            if 'status' in data['result']:
                if data['result']['status'] == "SUCCESS":
                    success = True
                    betid = data['result']['instructionReports'][0]['instruction']['betId']
                    sizecancelled = data['result']['instructionReports'][0]['sizeCancelled']
                    datecancelled = helpers.timestamp_todatetime(data['result']['instructionReports'][0]['cancelledDate'])
                    details = pd.DataFrame({'betId': [betid], 'sizeCancelled': [sizecancelled],
                                            'cancelledDate': [datecancelled]})

                else:
                    success = False
                    details = "Bet cancellations failed, received following json response: {0}".format(str(data))
            else:
                success = False
                details = "Bet placement failed, no status sent back in response"
        else:
            success = False
            try:
                errorcode = data['error']['data']['APINGException']['errorCode']
                errordetails = data['error']['data']['APINGException']['errorDetails']
                details = "Failed to cancel bet, error code: {0}, error details: {1}".format(errorcode, errordetails)
            except KeyError:
                try:
                    error = helpers.extract_error(result)
                    details = "Failed to cancel bet, error details: {0}".format(error)
                except:
                    details = "Failed to cancel bet, unrecognized error code."

    return success, details
