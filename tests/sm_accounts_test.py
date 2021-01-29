import sys
import configparser
import os
import pandas as pd
import datetime

sys.path.append("../smarketswrapper")
# Importing modules
import sessions
import accounts


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

        # Test 1 - should be success
        success, details = accounts.get_account_info(sesstoken)

        if success and type(details)==dict:
            print("Test 1 for getting account details passed.")
        else:
            print("Test 1 for getting account details failed, success: {0}, details: {1}".format(success, details))

        # Test 2 - should fail

        success, details = accounts.get_account_info(sesstoken+"a")

        if success==False and type(details) == str:
            print("Test 2 for getting account details passed.")
        else:
            print("Test 2 for getting account details failed, success: {0}, details: {1}".format(success, details))

        # Test 3 - should be success
        success, details = accounts.get_account_statement(sesstoken)


        if success and type(details)==pd.DataFrame:
            print("Test 3 for getting account statement passed.")
        else:
            print("Test 3 for getting account details failed, success: {0}, details: {1}".format(success, details))


        # Test 4 - should be failure
        success, details = accounts.get_account_statement(sesstoken+"a")

        if success==False and type(details) == str:
            print("Test 4 for getting account statement passed.")
        else:
            print("Test 4 for getting account details failed, success: {0}, details: {1}".format(success, details))

        # Test 5 - should be success with dataframe length = 0
        success, details = accounts.get_account_statement(sesstoken,
            {'start':datetime.datetime(2020,1, 1), 'end':datetime.datetime(2020, 1, 20)})

        if success and type(details) == pd.DataFrame and len(details)==0:
            print("Test 5 for getting account statement passed.")
        else:
            print("Test 5 for getting account details failed, success: {0}, details: {1}".format(success, details))

        # Test 6 - should be success with dataframe length > 0
        success, details = accounts.get_account_statement(sesstoken,
                                                          {'start': datetime.datetime(2021, 1, 1),
                                                           'end': datetime.datetime(2021, 2, 1)})

        if success and type(details) == pd.DataFrame and len(details)>0:
            print("Test 6 for getting account statement passed.")
        else:
            print("Test 6 for getting account details failed, success: {0}, details: {1}".format(success, details))

    else:
        print("Failed to generate a session token, cannot perform tests.")


main()