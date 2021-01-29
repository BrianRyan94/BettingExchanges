from smarketswrapper import helpers
import pandas as pd
import json


def place_order(sesstoken, contractid, marketid, price, quantity, side, bettype):

    """Returns a dictionary of the bet placement details.

                       Parameters:
                           sessiontoken (str): Smarkets session token
                           contractid (str/int): ContractID chosen - for example Man Utd in the Man Utd vs Arsenal Winners market
                           price (float): limit price (expressed in terms of probabilities)
                           quantity (float): the quantity in the account currency that you want to place
                           side (buy/sell): Indicate if you are backing or laying
                           bettype (string): The bettype you want (e.g. good_til_halted/good_till_cancelled/keep_in_play/
                           immediate_or_cancel)

                       Returns:
                           success (boolean): True if api call is successful, else false

                           details (dictionary/string): If success is true then a dictionary with the bet
                           placement details, otherwise an error. Note that the success field does not necessarily
                           mean the bet is placed - it just means the request and response is all as expected. The
                           response might be that your bet was rejected."""

    price = helpers.odds_inverter(float(price))
    quantity = helpers.size_inverter(quantity, price)

    payload = {
        'contract_id': str(contractid),
        'market_id': str(marketid),
        'price': price,
        'quantity': int(quantity),
        'side': side,
        'type': bettype
    }

    headers = {"Authorization": "Session-Token {0}".format(sesstoken)}

    result = helpers.order_req(headers, "post", payload)


    if result.status_code == 200:
        success = True
        details = result.json()
        details.update({'real_quantity': helpers.size_transformer(details['quantity'], details['price'])})

    else:
        success = False
        try:
            details = "Status code {0} received, error type: " \
                      "{1}".format(str(result.status_code), result.json()['error_type'])
        except:
            details = "Status code {0} received, error type: " \
                      "{1}".format(str(result.status_code), str(result.json()))

    return success, details


def get_order_log(sesstoken, timerange={}):


    """Returns a dictionary of dataframes - 3 dataframes, the keys
    are live/fills/pending all corresponding to those order types.

                       Parameters:
                           sessiontoken (str): Smarkets session token
                           timerange (dictionary): Dictionary with 2 values, start/end. Both
                           values must be datetime types.

                       Returns:
                           success (boolean): True if api call is successful, else false

                           details (dictionary/string): If success is true then a dictionary with the
                           dataframes of orders - that is a 'live' dataframe for live orders, a 'pending'
                           dataframe for filled but pending confirmation orders, 'fills' dataframe
                           which shows executed orders with price & volume details."""

    headers = {"Authorization": "Session-Token {0}".format(sesstoken)}

    params = {"limit": ["100"]}

    if len(timerange) != 0:
        start_ts = helpers.datetime_totimestamp(timerange['start'])
        end_ts = helpers.datetime_totimestamp(timerange['end'])
        params.update({'created_datetime_min':[start_ts]})
        params.update({'created_datetime_max':[end_ts]})

    result = helpers.order_req(headers, "get", params)

    if result.status_code == 200:
        data = result.json()
        if 'orders' in data:
            success = True
            data = data['orders']
            data_dict = {}
            for fld in ['average_price_matched', 'contract_id', 'created_datetime', 'id', 'market_id', 'price',
                        'quantity_user_currency', 'quantity_filled_user_currency', 'quantity_unfilled_user_currency',
                        'side', 'state',
                        'quantity_filled_pending_user_currency']:
                data_dict[fld] = [x[fld] for x in data]
            details = pd.DataFrame(data_dict)


            details = details.rename(columns={'average_price_matched': 'average_fill_px',
                                              'id': 'order_id'})
            details = details.sort_values(by='created_datetime', ascending=False)
            details = details[['order_id', 'created_datetime', 'contract_id', 'market_id',
                               'state', 'side', 'price', 'quantity_user_currency',
                               'quantity_filled_user_currency', 'quantity_unfilled_user_currency', 'average_fill_px',
                               'quantity_filled_pending_user_currency']]

            details['created_datetime'] = details['created_datetime'].apply(helpers.timestamp_todatetime)

            if len(details)==0:
                details['real_quantity'] = []
                details['real_quantity_filled'] = []
                details['real_quantity_unfilled'] = []
                details['real_quantity_pending_filled'] = []
            else:
                details['real_quantity'] = details[['quantity_user_currency', 'price']].apply(
                    helpers.size_transformer_series, axis=1)
                details['real_quantity_filled'] = details[['quantity_filled_user_currency', 'average_fill_px']].apply(
                    helpers.size_transformer_series, axis=1)
                details['real_quantity_unfilled'] = details[['quantity_unfilled_user_currency', 'price']].apply(
                    helpers.size_transformer_series, axis=1)
                details['real_quantity_pending_filled'] = details[
                    ['quantity_filled_pending_user_currency', 'average_fill_px']].apply(helpers.size_transformer_series,
                                                                                        axis=1)

            details['average_fill_px'] = details['average_fill_px'].apply(helpers.odds_transformer)
            details['price'] = details['price'].apply(helpers.odds_transformer)

            # Extract different order types
            fills_df = helpers.extract_order_type(details, "fills")
            live_df = helpers.extract_order_type(details, "live")
            pending_fills_df = helpers.extract_order_type(details, "pending")

            details = {'live': live_df, 'fills': fills_df, 'pending': pending_fills_df}

        else:
            success = False
            details = "Response code 200 but no orders found. Message received: {0}".format(str(result.json()))
    else:
        success = False
        try:
            details = "Status code {0} received, error type: " \
                      "{1}".format(str(result.status_code), result.json()['error_type'])
        except:
            details = "Status code {0} received, error type: " \
                      "{1}".format(str(result.status_code), str(result.json()))

    return success, details


def cancel_order(sesstoken, orderid=None):


    """Returns a string showing the details of the cancelled order.

                       Parameters:
                           sessiontoken (str): Smarkets session token
                           orderid *optional* (str/int): order id to cancel - if left blank then all orders cancelled.

                       Returns:
                           success (boolean): True if api call is successful, else false

                           details (string): If success is true then a string of the betfair response.
                           If success if false then a string detailing the error."""

    headers = {"Authorization": "Session-Token {0}".format(sesstoken)}

    if orderid == None:
        params = {}
    else:
        params = {'orderid': orderid}

    result = helpers.order_req(headers, "delete", params)

    if result.status_code == 200:
        data = result.json()
        success = True
        details = json.dumps(data)
    else:
        data = result.json()
        success = False
        details = json.dumps(data)

    return success, details
