""" standard """
import configparser as ConfigParser
import sys

""" custom """
from threatconnect import ThreatConnect

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

# Bulk Indicator object
indicators = tc.bulk_indicators()

owner = "*"

try:
    # retrieve the Indicators
    indicators.retrieve()
except RuntimeError as e:
    print(e)
    sys.exit(1)

col = {
    "Indicator": [],
    "Type": [],
    "Value": [],
    "Organization": [],
    "Rating": [],
    "Confidence": [],
    "DateAdded": [],
    "LastModified": [],
    "Description": [],
    "Source": [],
    "DNS": [],
    "Whois": [],
    "Active": [],
    "Observations": [],
    "Date Last Observed": [],
    "False Positives": [],
    "Date FP Last Reported": [],
    "Tags": []
}

for indicator in indicators:
    indicator.load_attributes()
    indicator.load_tags()
    for attr_obj in indicator.attributes:
        col["Type"].append(attr_obj.type)
        col["Value"].append(attr_obj.value)
        col[""]
