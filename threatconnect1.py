import configparser as ConfigParser
import sys
import pandas as pd
import os

from threatconnect1 import ThreatConnect
import owners
import util

class threatConnect1:

    def __init__(self):
    # config
    config_file = "tc.conf"
    f_name_directory = os.getcwd() + r"\csv"
    n_files = len(os.listdir(f_name_directory))
    filename = os.path.join(f_name_directory, "{}.csv".format(n_files))

    # retrieve configuration file
    config = ConfigParser.RawConfigParser()
    config.read(config_file)

    try:
        api_access_id = config.get('threatconnect', 'api_access_id')
        api_secret_key = config.get('threatconnect', 'api_secret_key')
        api_default_org = config.get('threatconnect', 'api_default_org')
        api_base_url = config.get('threatconnect', 'api_base_url')
        api_result_limit = int(50)
        #api_result_limit = int(config.get('threatconnect', 'api_result_limit'))
    except ConfigParser.NoOptionError:
        print('Could not retrieve configuration file.')
        sys.exit(1)

    tc = ThreatConnect(api_access_id, api_secret_key, api_default_org, api_base_url)
    tc.set_api_result_limit(api_result_limit)