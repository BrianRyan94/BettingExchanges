import sys
import configparser
import os
import pandas as pd

sys.path.append("../smarketswrapper")
# Importing modules
import sessions
import staticdata

pd.set_option('expand_frame_repr', False)

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

        # Test 1 for getting base events - should be success

        success, details = staticdata.get_base_events(sesstoken)

        #for future test
        golfid = list(details[details['Name']=='Golf']['ID'])[0]

        if success and type(details)==pd.DataFrame:
            print("Test 1 for getting base events passed.")
        else:
            print("Test 1 for getting base events failed, success:{0} error: {1}".format(success, details))

        # Test 2 - for getting child events

        success, details = staticdata.get_child_events(sesstoken, golfid, {'limit':[1000]})

        if success and type(details)==pd.DataFrame:
            print("Test 2 for getting child events passed.")
        else:
            print("Test 2 for getting child events failed, success:{0} error: {1}".format(success, details))

        # Test 3 - for getting child events. Should fail.

        success, details = staticdata.get_child_events(sesstoken, golfid+"a", {'limit': [1000]})

        if success==False and type(details) == str:
            print("Test 3 for getting child events passed.")
        else:
            print("Test 3 for getting child events failed, success:{0} error: {1}".format(success, details))

    else:
        print("Failed to generate a session token, cannot perform tests.")




main()

