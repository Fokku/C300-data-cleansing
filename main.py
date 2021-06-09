# standard
import configparser as ConfigParser
import sys
from threatconnect import ThreatConnect
import pandas as pd

import owners
import tocsv

# configuration file
config_file = "tc.conf"

# retrieve configuration file
config = ConfigParser.RawConfigParser()
config.read(config_file)

try:
    api_access_id = config.get('threatconnect', 'api_access_id')
    api_secret_key = config.get('threatconnect', 'api_secret_key')
    api_default_org = config.get('threatconnect', 'api_default_org')
    api_base_url = config.get('threatconnect', 'api_base_url')
    api_result_limit = int(config.get('threatconnect', 'api_result_limit'))
except ConfigParser.NoOptionError:
    print('Could not retrieve configuration file.')
    sys.exit(1)

tc = ThreatConnect(api_access_id, api_secret_key, api_default_org, api_base_url)
tc.set_api_result_limit(api_result_limit)

# Create objects
csv = tocsv.csv()

owners = owners.getOwnerNames()

owners = ["abuse.ch Feodo Tracker", "Botvrij IPs"]
for owner in owners:
    print("Retrieving indicators for " + owner + "...")

    indicators = tc.bulk_indicators()
    filter = indicators.add_filter()
    filter.add_owner(owner)

    try:
        # retrieve the Indicators
        indicators.retrieve()
    except RuntimeError as e:
        print(e)
        sys.exit(1)

    p_csv = csv.format(indicators)
    print(p_csv)

csv.tocsv(p_csv)
