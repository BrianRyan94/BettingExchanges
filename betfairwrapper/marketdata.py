import helpers
import pandas as pd
import datetime


def get_mkt_book(appkey, sessiontoken, marketid):
    data_type = "listMarketBook"

    """Retrieves the market meta data and live odds for a given market ID.

    Dataframe columns includes 3 layers of back and lay offers,
    last price, total traded and status. Returns a boolean indicating
    whether the query was successful, and a details object which is a dictionary including 
    a Metadata key (for market metadata) and an Odds key which contains the data frame of live odds. 
    If success==False, returns an error message."""

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
                back_data = [try_layer_else_0(x, 'availableToBack', i) for x in runners]
                lay_data = [try_layer_else_0(x, 'availableToLay', i) for x in runners]
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


success, details = get_mkt_book('u3aNksQGhdXhGldb', 'ZFQMOo7hUsfoamCdocvMsJLN3vGid5/iiP5WV4G4poA=', 1.177840678)
