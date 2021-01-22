import helpers
import pandas as pd



def get_live_odds(sesstoken, marketid, type):

    if type=="quote":
         endpoint = "markets/{0}/quotes/".format(str(marketid))
    elif type=="trade":
         endpoint = "markets/{0}/last_executed_prices/".format(str(marketid))

    headers = {"Authorization": "Session-Token {0}".format(sesstoken)}

    result = helpers.data_req(endpoint, headers)
    success = False
    if result.status_code==200:
        data = result.json()
        if type=="trade":
            if 'last_executed_prices' in data:
                data = data['last_executed_prices']
                if str(marketid) in data and len(data[str(marketid)])>0:
                    success = True
                    data = data[str(marketid)]
            if success==False:
                details = "Response received but no trades for market id {0} found".apply(marketid)
        elif type=="quote":
            if len(data)>0:
                success = True
            else:
                success = False
                details = "Response received but no quotes for market id {0} found".apply(marketid)

        if success:

            if type=="quote":
                details = helpers.parse_odds_to_df(data)

            elif type=="trade":
                details = helpers.parse_trades_to_df(data)

    return success, details
















