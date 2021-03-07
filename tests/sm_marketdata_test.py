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
    sesstoken = sesstoken['token']
    if success:

        ###Just for gettin a market id

        # Test 1 - should be success
        success, trades = marketdata.get_live_odds(sesstoken, [12304075, 10960825], "trade")

        if success and type(trades) == dict:
            print("Test 1 for getting trades passed.")
        else:
            print("Test 1 for getting trades failed, success: {0}, details: {1}".format(success, trades))

        success, quotes = marketdata.get_live_odds(sesstoken, [12304075,10960825], "quote")

        if success and type(quotes) == pd.DataFrame:
            print("Test 2 for getting quotes passed.")
        else:
            print("Test 2 for getting quotes failed, success: {0}, details: {1}".format(success, quotes))

        # Test 3 - should be success

        success, volume = marketdata.get_volume(sesstoken, 12304075)

        if success and type(volume)==pd.DataFrame:
            print("Test 3 for getting volumes passed.")
        else:
            print("Test 3 for getting volumes faild, success: {0}, details: {1}".format(success, volume))

        # Test 4 - should be failure

        success, volume = marketdata.get_volume(sesstoken+"a", 12304075)

        if success==False and type(volume) == str:
            print("Test 4 for getting volumes passed.")
        else:
            print("Test 4 for getting volumes failed, success: {0}, details: {1}".format(success, volume))


    else:
        print("Failed to generate a session token, cannot perform tests.")


main()
