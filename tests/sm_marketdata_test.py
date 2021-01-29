import sys
import configparser
import os
import pandas as pd

sys.path.append("../smarketswrapper")
# Importing modules
import sessions
import staticdata
import marketdata

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', None)

def parse_config():
    conf_path = os.path.dirname(__file__).replace("tests", "conf") + "/conf.conf"

    config = configparser.ConfigParser()
    config.read(conf_path)

    configs_dict = {}

    for field in config["details"]:
        configs_dict[field] = config["details"][field]

    return configs_dict


configs = parse_config()
uname = configs["sm_uname"]
pw = configs["sm_pw"]


def main():
    success, sesstoken = sessions.connect_session(uname, pw)

    if success:

        ###Just for gettin a market id
        success, details = staticdata.get_base_events(sesstoken)
        golfid = list(details[details['Name'] == 'Golf']['ID'])[0]
        success, details = staticdata.get_child_events(sesstoken, golfid, {'limit': [1000]})
        comp_id = list(details[details['Name']=='US Open 2021']['ID'])[0]
        success, details = staticdata.get_child_events(sesstoken, comp_id)
        bettable_id = list(details['ID'])[0]
        success, details = staticdata.get_market_types(sesstoken, bettable_id)
        winner_id = list(details[details['name'] == 'The US Open - Winner']['id'])[0]

        # Test 1 - should be success
        success, trades= marketdata.get_live_odds(sesstoken, winner_id, "trade")

        if success and type(trades)==pd.DataFrame:
            print("Test 1 for getting trades passed.")
        else:
            print("Test 1 for getting trades failed, success: {0}, details: {1}".format(success, trades))

        # Test 2 - should be success

        success, quotes = marketdata.get_live_odds(sesstoken, winner_id, "quote")

        if success and type(quotes) == pd.DataFrame:
            print("Test 2 for getting quotes passed.")
        else:
            print("Test 2 for getting quotes failed, success: {0}, details: {1}".format(success, quotes))

        # Test 3 - should be success

        success, volume = marketdata.get_volume(sesstoken, winner_id)

        if success and type(volume)==pd.DataFrame:
            print("Test 3 for getting volumes passed.")
        else:
            print("Test 3 for getting volumes faild, success: {0}, details: {1}".format(success, volume))

        # Test 4 - should be failure

        success, volume = marketdata.get_volume(sesstoken+"a", winner_id)

        if success==False and type(volume) == str:
            print("Test 4 for getting volumes passed.")
        else:
            print("Test 4 for getting volumes failed, success: {0}, details: {1}".format(success, volume))


    else:
        print("Failed to generate a session token, cannot perform tests.")


main()
