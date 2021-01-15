import sys
import configparser
import os
import pandas as pd

sys.path.append("../betfairwrapper")
# Importing modules
import sessions
import staticdata


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

if success == False:
    print("Failed to generate a session token, cannot perform tests")
else:

    # Test 1 for events
    success, events = staticdata.get_base_events(appkey, sesstoken)

    if success and type(events) == pd.DataFrame:
        print("Test 1 for getting base events successful")
    else:
        print("Test 1 for getting base events failed, success:{0}, details:{1}".format(success, events))

    # Test 2 for events
    success, events = staticdata.get_base_events(appkey + "a", sesstoken)

    if success == False and type(events) == str:
        print("Test 2 for getting base events successful")
    else:
        print("Test 2 for getting base events failed, success:{0}, details:{1}".format(success, events))

    # Test 3 for competitions
    success, competitions = staticdata.get_competitions(appkey, sesstoken, '3')

    if success and type(competitions) == pd.DataFrame:
        print("Test 3 for getting competitions successful")
    else:
        print("Test 3 for getting base events failed, success:{0}, details:{1}".format(success, competitions))

    # Test 4 for competitions
    success, competitions = staticdata.get_competitions(appkey, sesstoken)

    if success and type(competitions) == pd.DataFrame:
        print("Test 4 for getting competitions successful")
    else:
        print("Test 4 for getting base events failed, success:{0}, details:{1}".format(success, competitions))

    # Test 5 for competitions
    success, competitions = staticdata.get_competitions(appkey, sesstoken + "a")

    if success == False and type(competitions) == str:
        print("Test 5 for getting competitions successful")
    else:
        print("Test 5 for getting competitions failed, success:{0}, details:{1}".format(success, competitions))

    sessions.logout(sesstoken, appkey)
