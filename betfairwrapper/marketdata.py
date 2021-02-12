from betfairwrapper import helpers
import pandas as pd
import datetime


def get_mkt_book(appkey, sessiontoken, marketid):

    """Retrieves the market book for a given market ID.

                    Parameters:
                        appkey (str): Betfair Application Key
                        sessiontoken (str): Betfair session token
                        marketid (str/int): Market ID for which market book will be returned

                    Returns:
                        success (boolean): True if request is successful, else false

                        details (dictionary/string): If success is true then a dictionary 2 fields.
                        One field is metadata which has details on whether the odds are delayed,
                        what the market status is, what the bet delay is, what the total matched is.
                        The second field is a dataframe with 3 layers of market bids (backs) and
                        offers (lays). The odds are returned in implied probabilities (i.e. 0.05
                        corresponds to 20 on betfair decimal odds. If success==false, an error message."""

    data_type = "listMarketBook"
    params = {'marketIds': [marketid],
              'priceProjection': {"priceData": ["EX_ALL_OFFERS"]}}

    result = helpers.data_req(appkey, sessiontoken, data_type, params)

    if result.status_code == 200:
        if 'result' in result.json():
            try:
                data = result.json()['result'][0]
                runners = data['runners']
            except (IndexError, KeyError):
                return False, "No market book data found for market id {0}".format(str(marketid))

            success = True
            metadata = {'Delayed': data.get('isMarketDataDelayed', float("nan")),
                        'MarketStatus': data.get('status', float("nan")),
                        'betDelay': data.get('betDelay', float("nan")), 'inplay': data.get('inplay', float("nan")),
                        'totalmatched': data.get('totalMatched', float("nan")),'UpdateTime':datetime.datetime.now()}

            selectionids = [x['selectionId'] for x in runners]
            status = [x.get('status', float("nan")) for x in runners]
            lastprice = [helpers.odds_transformer(x.get('lastPriceTraded', float("nan"))) for x in runners]
            totalmatched = [x.get('totalMatched', float("nan")) for x in runners]

            def try_layer_else_0(layers_dict, fieldtype, index):
                try:
                    mktpacket = layers_dict['ex'][fieldtype][index]
                    return (helpers.odds_transformer(mktpacket['price']), mktpacket['size'])
                except:
                    return (0, 0)

            market_df = pd.DataFrame()
            market_df['SelectionID'] = selectionids
            market_df['Status'] = status
            market_df['lastprice'] = lastprice
            market_df['totalMatched'] = totalmatched

            for i in range(3):
                back_data = [try_layer_else_0(x, 'availableToLay', i) for x in runners]
                lay_data = [try_layer_else_0(x, 'availableToBack', i) for x in runners]
                market_df['BACK' + str(i)] = [x[0] for x in back_data]
                market_df['BACKSIZE' + str(i)] = [x[1] for x in back_data]
                market_df['LAY' + str(i)] = [x[0] for x in lay_data]
                market_df['LAYSIZE' + str(i)] = [x[1] for x in lay_data]

            details = {'Metadata': metadata, "Odds": market_df}
        else:
            success = False
            details = helpers.extract_error(result)
    else:
        success = False
        details = "Request for events failed, status code: {0}".format(str(result.status_code))

    return success, details



