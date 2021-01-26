import helpers
import pandas as pd


def place_order(sesstoken, contractid, marketid, price, quantity, side, bettype):
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


def get_order_log(sesstoken):
    ###Need to add time filters and sort out what is wrong with the quantities.

    headers = {"Authorization": "Session-Token {0}".format(sesstoken)}

    params = {"limit": ["100"]}

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

            # Extract the actual filled orders
            fills_df = details[['order_id', 'created_datetime', 'contract_id', 'market_id', 'state', 'side',
                                'average_fill_px', 'real_quantity_filled', 'quantity_filled_user_currency']]

            fills_df = fills_df[fills_df['quantity_filled_user_currency'] > 0]

            # Extract the live orders
            live_df = details[['order_id', 'price', 'real_quantity_unfilled', 'created_datetime',
                               'contract_id', 'market_id', 'state', 'side',
                               'quantity_unfilled_user_currency']]

            live_df = live_df[live_df['quantity_unfilled_user_currency'] > 0]

            # Extract the pending fills

            pending_fills_df = details[['order_id', 'created_datetime', 'contract_id', 'market_id', 'state', 'side',
                                        'average_fill_px', 'real_quantity_pending_filled',
                                        'quantity_filled_pending_user_currency']]

            pending_fills_df = pending_fills_df[pending_fills_df['quantity_filled_pending_user_currency'] > 0]

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
