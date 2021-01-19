import helpers
import datetime
import pandas as pd


def list_orders(appkey, sessiontoken, since=None, until=None):
    """Returns a dataframe of prior orders for the date range specified (if date range given

    Uses the default api settings - that is ordered by bet placed time. The date range
    filter also uses the bet placed time. Dataframe includes betid, marketid, selection id,
    the size matched/cancelled/voided, the average price matched, the size remaining and
    the order status. Follows convention of a boolean success=True/False being returned
    first followed by a variable, "details" which corresponds to the dataframe if success=True,
    otherwise an error message"""

    data_type = "listCurrentOrders"

    params = {"dateRange": {}}

    if since != None:
        since = helpers.datetime_totimestamp(since)
        until = helpers.datetime_totimestamp(until)
        params["dateRange"].update({"from": since})
        params["dateRange"].update({"to": until})

    result = helpers.data_req(appkey, sessiontoken, data_type, params)

    if result.status_code == 200:

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

        else:
            success = False
            details = helpers.extract_error(result)
    else:
        success = False
        details = "Request for order details failed, status code: {0}".format(str(result.status_code))

    return success, details


def placeOrder(appkey, sessiontoken, marketid, selectionid, side, amount, limitpx):
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
                    details = "Bet placement failed, received json response with succes={0}".format(str(status))
            else:
                success = False
                details = "Bet placement failed, no status sent back in response"
        else:
            success = False
            try:
                errorcode = data['error']['data']['APINGException']['errorCode']
                errordetails = data['error']['data']['APINGException']['errorDetails']
                details = "Failed to place bet, error code: {0}, error details: {1}".format(errorcode, errordetails)
            except KeyError:
                try:
                    error = helpers.extract_error(result)
                    details = "Failed to place bet, error details: {0}".format(error)
                except:
                    details = "Failed to place bet, unrecognized error code."

    return success, details

def cancelOrder(appkey, sessiontoken, marketid, betid, sizereduction):

    data_type = "cancelOrders"

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
                    status = data['result']['status']
                    details = "Bet cancellations failed, received json response with success={0}".format(str(status))
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



# [{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/placeOrders", "params": {"marketId":"1.177752745","instructions":[{"selectionId":"6611396","handicap":"0","side":"BACK","orderType":"LIMIT","limitOrder":{"size":"2","price":"1.01"}}]}, "id": 1}]

# {'jsonrpc': '2.0', 'error': {'code': -32099, 'message': 'ANGX-0002', 'data': {'APINGException': {'requestUUID': 'ie2-ang22a-prd-01140948-0009f9ebb8', 'errorCode': 'INVALID_INPUT_DATA', 'errorDetails': 'market id passed is invalid'}, 'exceptionname': 'APINGException'}}, 'id': 1}
