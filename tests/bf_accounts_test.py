import sys
import configparser
import os
import pandas as pd

sys.path.append("../betfairwrapper")
# Importing modules
import sessions
import accounts


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
    success, details = accounts.get_account_balance(appkey, sesstoken)

    if success and type(details) == dict:
        print("Test 1 for getting account funds successful")
    else:
        print("Test 1 for getting account funds failed, success:{0}, details:{1}".format(success, details))


    # Test 2 for account funds - should be unsuccessful

    success, details = accounts.get_account_balance(appkey+"a", sesstoken)

    if success==False and type(details) == str:
        print("Test 2 for getting account funds successful")
    else:
        print("Test 2 for getting account funds failed, success:{0}, details:{1}".format(success, details))


if success == False:
    print("Failed to generate a session token, cannot perform tests")
else:
    main()
    sessions.logout(sesstoken, appkey)
