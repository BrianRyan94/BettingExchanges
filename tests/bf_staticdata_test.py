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

def main():

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

    # Test 6 for market types
    success, markettypes = staticdata.get_mkt_types_for_comp(appkey, sesstoken, 345369)

    if success and type(markettypes) == pd.DataFrame:
        print("Test 6 for getting market types successful")
    else:
        print("Test 6 for getting market types failed, success:{0}, details:{1}".format(success, markettypes))

    # Test 7 for market types
    success, markettypes = staticdata.get_mkt_types_for_comp(appkey + "a", sesstoken, 345369)

    if success==False and type(markettypes) == str:
        print("Test 7 for getting market types successful")
    else:
        print("Test 7 for getting market types failed, success:{0}, details:{1}".format(success, markettypes))

    # Test 8 for timeranges

    success, timeranges = staticdata.get_timerange_competition(appkey, sesstoken, 345369)

    if success and type(timeranges) == pd.DataFrame:
        print("Test 8 for getting market types successful")
    else:
        print("Test 8 for getting market types failed, success:{0}, details:{1}".format(success, timeranges))

    # Test 9 for timeranges
    success, timeranges = staticdata.get_timerange_competition(appkey, sesstoken, 34536900000)

    if success and type(timeranges) == pd.DataFrame:
        print("Test 9 for getting time ranges successful")
    else:
        print("Test 9 for getting time ranges failed, success:{0}, details:{1}".format(success, timeranges))

    #Test 10 for timeranges

    success, timeranges = staticdata.get_timerange_competition(appkey + "a", sesstoken, 34536900000)

    if success==False and type(timeranges) == str:
        print("Test 10 for getting time ranges successful")
    else:
        print("Test 10 for getting time ranges failed, success:{0}, details:{1}".format(success, timeranges))

    # Test 11 for runner names: valid market id
    success, runnernames = staticdata.get_runner_names(appkey, sesstoken, 1.177840678)

    if success and type(runnernames) == pd.DataFrame:
        print("Test 11 for getting runner names successful")
    else:
        print("Test 11 for getting runner names failed, success:{0}, details:{1}".format(success, runnernames))

    # Test 12 for runner names: invalid market id
    success, runnernames = staticdata.get_runner_names(appkey, sesstoken, 1111)

    if success==False and type(runnernames) == str:
        print("Test 12 for getting runner names successful")
    else:
        print("Test 12 for getting runner names failed, success:{0}, details:{1}".format(success, runnernames))

    # Test 13 for runner names: invalid authentication
    success, runnernames = staticdata.get_runner_names(appkey + "a", sesstoken, 1111)

    if success == False and type(runnernames) == str:
        print("Test 13 for getting runner names successful")
    else:
        print("Test 13 for getting runner names failed, success:{0}, details:{1}".format(success, runnernames))

    sessions.logout(sesstoken, appkey)

if success == False:
    print("Failed to generate a session token, cannot perform tests")
else:
    main()
    sessions.logout(sesstoken, appkey)
