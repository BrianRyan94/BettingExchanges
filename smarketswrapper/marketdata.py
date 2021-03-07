from smarketswrapper import helpers
import pandas as pd


def get_live_odds(sesstoken, marketids, type):
    """Returns a dataframe of live market details for either quotes or trades.

                    Parameters:
                        sessiontoken (str): Smarkets session token
                        marketid list: (str/int): MarketIDs for which odds/trades are required
                        type (quote/trade): Determines if market quotes or trades are returned

                    Returns:
                        success (boolean): True if api call is successful, else false

                        details (Dataframe/string): If success is true then a dataframe with
                        live market odds/trades. If success==False, an error message."""

    marketidstring = ",".join([str(x) for x in marketids])
    if type=="quote":
         endpoint = "markets/{0}/quotes/".format(marketidstring)
    elif type=="trade":
         endpoint = "markets/{0}/last_executed_prices/".format(marketidstring)

    headers = {"Authorization": "Session-Token {0}".format(sesstoken)}

    result = helpers.data_req(endpoint, headers)
    success = False
    if result.status_code==200:
        data = result.json()
        if type=="trade":
            if 'last_executed_prices' in data:
                data = data['last_executed_prices']
                success = True
            if success==False:
                details = "Response received but no trades for market ids {0} found".apply(marketidstring)
        elif type=="quote":
            if len(data)>0:
                success = True
            else:
                success = False
                details = "Response received but no quotes for market ids {0} found".apply(marketidstring)

        if success:
            if type=="quote":
                details = helpers.parse_odds_to_df(data)

            elif type=="trade":
                details = {}
                for marketid in list(data.keys()):
                    tradedf = helpers.parse_trades_to_df(data[marketid])
                    details[marketid] = tradedf



    else:
        success = False
        details = str(result.json())
    return success, details

def get_volume(sesstoken, marketid):

    """Returns a dataframe with 1 row indicating the market ID and volume for that market.

    **I believe the volume is returned in GBP instead of account currency at present**

                       Parameters:
                           sessiontoken (str): Smarkets session token
                           marketid (str/int): MarketID for which volume is required

                       Returns:
                           success (boolean): True if api call is successful, else false

                           details (Dataframe/string): If success is true then a dataframe with
                           1 row, columns market id and volume. If success==False, an error message."""

    endpoint = "markets/{0}/volumes/".format(str(marketid))

    headers = {"Authorization": "Session-Token {0}".format(sesstoken)}

    result = helpers.data_req(endpoint, headers)

    if result.status_code==200:
        data = result.json()
        if 'volumes' in data and len(data['volumes'])>0:
            success = True
            data = data['volumes'][0]
            details = pd.DataFrame({'market_id':[data['market_id']], 'volume':[data['volume']]})
        else:
            success = False
            details = str(data)
    else:
        success = False
        error_code = str(result.status_code)
        error_details = str(result.json())
        details = "Failed, response code {0}, error details: {1}".format(str(error_code), str(error_details))

    return success, details





















