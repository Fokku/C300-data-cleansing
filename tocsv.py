import configparser as ConfigParser
import sys
import pandas as pd
import os

from threatconnect import ThreatConnect
import owners

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

# Bulk Indicator object
indicators = tc.bulk_indicators()

owner = "abuse.ch Feodo Tracker"

filter = indicators.add_filter()
filter.add_owner(owner)

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
    #TODO IN CASE MENG HONG NEEDS IT
    #"DNS": [],
    #"Whois": [],
    #"Active": [],
    #"Observations": [],
    #"Date Last Observed": [],
    #"False Positives": [],
    #"Date FP Last Reported": [],
    "Tags": []
}

print(indicators[0].attributes)
print(indicators[0].tags)
print(dir(indicators[1]))
for indicator in indicators:
    tagname = ""
    indicator.load_attributes()
    indicator.load_tags()
    col["Indicator"].append(indicator.indicator)
    col["Type"].append(indicator.type)
    col["Organization"].append(indicator.owner_name)
    col["Rating"].append(indicator.rating)
    col["Confidence"].append(indicator.confidence)
    col["DateAdded"].append(indicator.date_added)
    col["Description"].append(indicator.description)
    col["Source"].append((indicator.source))
    if len(indicator.tags) > 0:
        for tag in indicator.tags:
            tagname += tag.name + ";"
    else:
        tagname = "0"
    col["Tags"].append(tagname)
    for attr_obj in indicator.attributes:
        col["Value"].append(attr_obj.value)
        col["LastModified"].append(attr_obj.last_modified)

print("working")
df = pd.DataFrame(col)
print(col)
df.to_csv(filename)
