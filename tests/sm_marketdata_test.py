import sys
import configparser
import os
import pandas as pd

sys.path.append("../smarketswrapper")
# Importing modules
import sessions
import staticdata
import marketdata

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

        success, details = staticdata.get_base_events(sesstoken)
        golfid = list(details[details['Name'] == 'Golf']['ID'])[0]
        success, details = staticdata.get_child_events(sesstoken, golfid, {'limit': [1000]})
        comp_id = list(details[details['Name']=='Abu Dhabi Hsbc Championship 2021']['ID'])[0]
        success, details = staticdata.get_child_events(sesstoken, comp_id)
        bettable_id = list(details['ID'])[0]
        success, details = staticdata.get_market_types(sesstoken, bettable_id)

        print(details)

    else:
        print("Failed to generate a session token, cannot perform tests.")


main()
