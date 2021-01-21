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


        success, details = staticdata.get_base_events(sesstoken)
        golfid = list(details[details['Name'] == 'Golf']['ID'])[0]
        success, details = staticdata.get_child_events(sesstoken, golfid, {'limit': [1000]})
        comp_id = list(details[details['Name'] == 'Abu Dhabi Hsbc Championship 2021']['ID'])[0]
        success, details = staticdata.get_child_events(sesstoken, comp_id)
        bettable_id = list(details['ID'])[0]

        # Test 4 - should be a success
        success, details = staticdata.get_market_types(sesstoken, bettable_id)

        winner_id = list(details[details['name']=='Winner']['id'])[0]


        if success and type(details) == pd.DataFrame:
            print("Test 4 for getting market types passed")
        else:
            print("Test 4 for getting market types failed, success: {0}, details: {1}".format(success, details))

        # Test 5 for getting market data types - should fail.

        success, details = staticdata.get_market_types(sesstoken + "a", 9999)

        if success == False and type(details) == str:
            print("Test 5 for getting market types passed")
        else:
            print("Test 5 for getting market types failed, success: {0}, details: {1}".format(success, details))

        # Test 6 for getting contracts for market id - should succeed

        success, details = staticdata.get_contracts_for_market(sesstoken, winner_id)

        if success and type(details)==pd.DataFrame:
            print("Test 6 for getting contracts passed")
        else:
            print("Test 6 for getting contracts failed, success: {0}, details: {1}".format(success, details))

        # Test 7 for getting contracts for market id - should fail

        success, details = staticdata.get_contracts_for_market(sesstoken, 101)

        if success==False and type(details) == str:
            print("Test 6 for getting contracts passed")
        else:
            print("Test 7 for getting contracts failed, success: {0}, details: {1}".format(success, details))

    else:
        print("Failed to generate a session token, cannot perform tests.")




main()

