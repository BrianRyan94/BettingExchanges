import sys
import configparser
import os

sys.path.append("../betfairwrapper")
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

###Testing session management

appkey = configs["app_key"]
uname = configs["uname"]
certpath = configs["cert_path"]
keypath = configs["key_path"]
pw = configs["pw"]

###Getting session token

def sess_token_test():
    ##should be successful
    ##Test 1
    success, output = sessions.get_sess_token(certpath, keypath, uname,                                       pw)
    if success==True and type(output)==str:
        print("Session Token Test 1 passed")
    else:
        print("***TEST FAILED: Session Token request, test 4.")

        ##Test 2
    success, output = sessions.get_sess_token(certpath, keypath, uname + "a",
                                              pw)
    if success == False and "Invalid Login" in output:
        print("Session Token Test 2 passed")
    else:
        print("***TEST FAILED: Session Token request, test 2.")

    ##Test 3
    success, output = sessions.get_sess_token(certpath, keypath, uname,
                                              pw + "a")
    if success == False and "Invalid Login" in output:
        print("Session Token Test 3 passed")
    else:
        print("***TEST FAILED: Session Token request, test 3.")

    sessions.logout(output, appkey)

def keep_alive_test():
    success, output = sessions.get_sess_token(certpath, keypath, uname, pw)

    if success==False:
        print("Failed to generate a session token, cannot perform tests")
    else:
        #Test 1 should be a success
        success, response = sessions.extend_session(output, appkey)

        if success and response=='':
            print("Test 1 passed for extending session.")
        else:
            print("Test 1 failed for extending session")
            print("Success returned {0}, output returned {1}".format(success, response))

        #Test 2 should fail and return NO_SESSION
        success, response = sessions.extend_session(output+ "x", appkey)

        if success==False and "NO_SESSION" in response:
            print("Test 2 passed for extending session")

        else:
            print("Test 2 failed for extending session")
            print("Success returned {0}, output returned {1}".format(success, response))

        sessions.logout(output, appkey)

def logout_test():
    success, output = sessions.get_sess_token(certpath, keypath, uname, pw)
    print(output)

    if success == False:
        print("Failed to generate a session token, cannot perform tests")
    else:

        #Test 1 should be a success
        success, response = sessions.logout(output, appkey)
        if success:
            print("Test 1 passed for logging out")
        else:
            print("Test 1 failed for extending session")
            print("Success returned {0}, output returned {1}".format(success, response))

        # Test 1 should be a success
        success, response = sessions.logout(output+"x", appkey)
        if success==False and "NO_SESSION" in response:
            print("Test 2 passed for logging out")
        else:
            print("Test 2 failed for extending session")
            print("Success returned {0}, output returned {1}".format(success, response))

            



sess_token_test()
keep_alive_test()
#logout_test()

