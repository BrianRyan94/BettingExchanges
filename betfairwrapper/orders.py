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

    params = {"dateRange":{}}

    if since!=None:
        since = helpers.datetime_totimestamp(since)
        until = helpers.datetime_totimestamp(until)
        params["dateRange"].update({"from":since})
        params["dateRange"].update({"to":until})

    result = helpers.data_req(appkey, sessiontoken, data_type, params)

    if result.status_code == 200:

        if 'result' in result.json():
            success = True
            data = result.json()['result']['currentOrders']
            df_dict = {}
            for fld in ["betId", "marketId", "selectionId", "side", "status",
                        "orderType", "placedDate", "matchedDate","averagePriceMatched",
                        "sizeMatched", "sizeCancelled", "sizeVoided", "sizeRemaining"]:
                df_dict[fld] = [x.get(fld,"NotFound") for x in data]
            df_dict["price"] = [x.get("priceSize", {}).get("price","NotFound") for x in data]
            df_dict["size"] = [x.get("priceSize", {}).get("size", "NotFound") for x in data]

            details = pd.DataFrame(df_dict)

        else:
            success = False
            details = helpers.extract_error(result)
    else:
        success = False
        details = "Request for order details failed, status code: {0}".format(str(result.status_code))

    return success, details
