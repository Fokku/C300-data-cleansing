""" standard """
import configparser as ConfigParser
import json
from random import randint
import re
import sys

""" custom """
from threatconnect import ThreatConnect
from threatconnect.Config.FilterOperator import FilterOperator
from threatconnect.Config.ResourceType import ResourceType
from threatconnect.RequestObject import RequestObject
from threatconnect.Config.IndicatorType import IndicatorType

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

tc = ThreatConnect(api_access_id, api_secret_key, api_default_org, api_base_url)

# Bulk Indicator object
indicators = tc.bulk_indicators()

owner = 'BruteForceBlocker Blocklist'

# add a Filter and Post Filters

try:
    filter1 = indicators.add_filter()
    filter1.add_owner(owner)
    # only download Indicators with a confidence rating greater than or equal to 75
    #filter1.add_pf_confidence(75, FilterOperator.GE)
    # only download Indicators with a threat rating greater than 2.5
    #filter1.add_pf_rating('2.5', FilterOperator.GT)
except AttributeError as e:
    print(e)
    sys.exit(1)

try:
    # retrieve the Indicators
    indicators.retrieve()
except RuntimeError as e:
    print(e)
    sys.exit(1)

# iterate through the results
for indicator in indicators:
    print(indicator.csv_header)
    print(indicator.csv)
    print('')
    # if the Indicator is a File Indicator or custom Indicator, print it out appropriately
    if isinstance(indicator.indicator, dict):
        for indicator_type, indicator_value in indicator.indicator.items():
            print('{0}: {1}'.format(indicator_type, indicator_value))
    else:
        print(indicator.indicator)


    print(indicator.tags)