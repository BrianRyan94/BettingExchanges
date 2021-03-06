import sys
import configparser
import os
import pandas as pd

sys.path.append("../betfairwrapper")
# Importing modules
import sessions
import marketdata

pd.set_option('display.expand_frame_repr', False)


def parse_config():
    conf_path = os.path.dirname(__file__).replace("tests", "conf") + "/conf.conf"

    config = configparser.ConfigParser()
    config.read(conf_path)

    configs_dict = {}

    for field in config["details"]:
        configs_dict[field] = config["details"][field]

    return configs_dict


configs = parse_config()
appkey = configs["app_key"]
uname = configs["uname"]
certpath = configs["cert_path"]
keypath = configs["key_path"]
pw = configs["pw"]

success, sesstoken = sessions.get_sess_token(certpath, keypath, uname, pw)

def main():

    # Test 1 for marketdata - valid market id
    success, details = marketdata.get_mkt_book(appkey, sesstoken, ['1.178793070','1.170182528'])
    print(details)
    if success and type(details) == dict:
        print("Test 1 for getting market book successful")
    else:
        print("Test 1 for getting market book failed, success:{0}, details:{1}".format(success, details))

    # Test 2 for marketdata - invalid market id
    success, details = marketdata.get_mkt_book(appkey, sesstoken, 9999)

    if success == False and type(details) == str:
        print("Test 2 for getting market book successful")
    else:
        print("Test 2 for getting market data failed, success:{0}, details:{1}".format(success, "dictionary returned"))

    # Test 3 for market data - invaid authentication
    success, details = marketdata.get_mkt_book(appkey, sesstoken+"a", 9999)

    if success == False and type(details) == str:
        print("Test 3 for getting market book successful")
    else:
        print("Test 3 for getting market data failed, success:{0}, details:{1}".format(success, "dictionary returned"))

    sessions.logout(sesstoken, appkey)

if success == False:
    print("Failed to generate a session token, cannot perform tests")
else:
    main()
    sessions.logout(sesstoken, appkey)
