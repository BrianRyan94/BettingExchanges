import sys
import configparser
import os
import pandas as pd
import datetime

sys.path.append("../betfairwrapper")
# Importing modules
import sessions
import orders


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

    # Test 1 for account funds - should be successful
    success, details = orders.list_orders(appkey, sesstoken)


    if success and type(details) == pd.DataFrame:
        print("Test 1 for getting order details successful")
    else:
        print("Test 1 for getting order details failed, success:{0}, details:{1}".format(success, details))


    # Test 2 for order details - should be unsuccessful

    success, details = orders.list_orders(appkey+"a", sesstoken)

    if success==False and type(details) == str:
        print("Test 2 for getting order details successful")
    else:
        print("Test 2 for getting order details failed, success:{0}, details:{1}".format(success, details))

    # Test 3 for order details including time ranges - should be successful

    success, details = orders.list_orders(appkey, sesstoken, datetime.datetime(2021, 1, 17, 13, 45, 0), datetime.datetime(2021, 1, 17, 14, 00, 30))

    if success and type(details) == pd.DataFrame:
        print("Test 3 for getting order details successful")
    else:
        print("Test 3 for getting order details failed, success:{0}, details:{1}".format(success, details))


if success == False:
    print("Failed to generate a session token, cannot perform tests")
else:
    main()
    sessions.logout(sesstoken, appkey)
