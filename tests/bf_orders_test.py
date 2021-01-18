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
pd.set_option('display.expand_frame_repr', False)
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

    success, details = orders.list_orders(appkey, sesstoken, datetime.datetime(2021, 1, 17, 13, 42, 0), datetime.datetime(2021, 1, 19, 23, 59, 00))
    print(details)
    if success and type(details) == pd.DataFrame:
        print("Test 3 for getting order details successful")
    else:
        print("Test 3 for getting order details failed, success:{0}, details:{1}".format(success, details))

    # Test 4 for placing an order - should be successful
    #success, details = orders.placeOrder(appkey, sesstoken, 1.177655531, 1222347, "BACK", 2, 1.05)

    #if success and type(details) == pd.DataFrame:
    #    print("Test 4 for placing order successful")
    #else:
    #    print("Test 4 for placing order failed, success:{0}, details:{1}".format(success, details))

    # Test 5 for placing an order - should be unsuccessful due to invalid market id

    success, details = orders.placeOrder(appkey, sesstoken, 9999, 1222347, "BACK", 2, 1.4)

    if success==False and type(details) == str:
        print("Test 5 for placing order successful")
    else:
        print("Test 5 for placing order failed, success:{0}, details:{1}".format(success, details))

    # Test 6 for placing an order - should be unsuccessful due to invalid app key

    success, details = orders.placeOrder(appkey+"a", sesstoken, 1.177655531, 1222347, "BACK", 2, 1.4)

    if success == False and type(details) == str:
        print("Test 6 for placing order successful")
    else:
        print("Test 6 for placing order failed, success:{0}, details:{1}".format(success, details))




if success == False:
    print("Failed to generate a session token, cannot perform tests")
else:
    main()
    sessions.logout(sesstoken, appkey)
