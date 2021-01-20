import configparser
import os
import sys


sys.path.append("../smarketswrapper")
# Importing modules
import sessions


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

# Test 1 - should be successful

def main():
    # Test 1 - generating session token should be successful
    success, details = sessions.connect_session(uname, pw)

    if success:
        print("Test 1 to generate a session token passed")
    else:
        print("Test 1 to generate a session token failed, error: {0}".format(details))

    # Test2 - generating session token should be unsuccessful
    success, details = sessions.connect_session(uname + "A","A")

    if success==False:
        print("Test 2 to generate a session token passed")
    else:
        print("Test 2 to generate a session token failed, error: {0}".format(details))

main()