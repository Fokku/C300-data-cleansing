# imports
import configparser as ConfigParser
import sys
from threatconnect import ThreatConnect
from threatconnect.Config.FilterOperator import FilterOperator
import pandas as pd
import datetime
import os

import owners
import tocsv

# config stuff
config_file = "tc.conf"
config = ConfigParser.RawConfigParser()
config.read(config_file)

try:
    api_access_id = config.get('threatconnect', 'api_access_id')
    api_secret_key = config.get('threatconnect', 'api_secret_key')
    api_default_org = config.get('threatconnect', 'api_default_org')
    api_base_url = config.get('threatconnect', 'api_base_url')
    api_result_limit = int(config.get('threatconnect', 'api_result_limit'))
    api_export_days = int(config.get('threatconnect', 'api_export_days'))
except ConfigParser.NoOptionError:
    print('Could not retrieve configuration file.')
    sys.exit(1)

tc = ThreatConnect(api_access_id, api_secret_key, api_default_org, api_base_url)
tc.set_api_result_limit(api_result_limit)

# initializing stuff
csv = tocsv.csv()

# directory configurations // idea: set it in config file
f_name_directory = os.getcwd() + r"\csv"
n_files = len(os.listdir(f_name_directory))
if n_files > 0:
    print("CSV file already exists in {}".format(f_name_directory))
    print("Deleting csv file")
    if not bool((input("Press ENTER to continue...\n"))):
        os.remove(path=f_name_directory + r"\1.csv")
    else:
        raise AssertionError
filename = os.path.join(f_name_directory, "{}.csv".format(n_files))

# calc date
today = datetime.datetime.today()
delta = datetime.timedelta(days=api_export_days)
previous_days_datestamp = (today - delta).isoformat() + 'Z'

owners = owners.getOwnerNames()
print("Owner list: " + str(owners))

# TESTING PURPOSES
# owners = ["abuse.ch Feodo Tracker", "Botvrij IPs"]
# owners = ["Firebog Prigent Phishing Domains", 'hpHosts Malware Distribution Domains', 'abuse.ch Zeus Tracker', 'hpHosts Phishing Domains']
owners = ["Blocklist.de SIP IPs", "VXVault", "DShield.org Recommended Blocklist CIDRs"]

for owner in owners:
    print("Retrieving indicators for " + owner + "...")

    indicators = tc.bulk_indicators()
    i_filter = indicators.add_filter()
    i_filter.add_owner(owner)

    # special lil filter for indicators added greater than a week ago
    # batch retrieve every week | can be changed in config
    i_filter.add_pf_date_added(previous_days_datestamp, FilterOperator.GT)

    try:
        # retrieve the Indicators
        indicators.retrieve()
    except RuntimeError as e:
        print(e)
        sys.exit(1)

    p_csv = csv.format(indicators)
    print(p_csv)

csv.tocsv(p_csv, directory=filename, logging=True)
