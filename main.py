try:
    import ConfigParser
except:
    import configparser as ConfigParser
import sys

from threatconnect import ThreatConnect

config = ConfigParser.RawConfigParser()
config.read('./tc.conf')

try:
    api_access_id = config.get('threatconnect', 'api_access_id')
    api_secret_key = config.get('threatconnect', 'api_secret_key')
    api_default_org = config.get('threatconnect', 'api_default_org')
    api_base_url = config.get('threatconnect', 'api_base_url')
except ConfigParser.NoOptionError:
    print('Could not read configuration file.')
    sys.exit(1)

tc = ThreatConnect(api_access_id, api_secret_key, api_default_org, api_base_url)

# instantiate Owners object
owners = tc.owners()

try:
    # retrieve the Owners
    owners.retrieve()
except RuntimeError as e:
    print('Error: {0}'.format(e))
    sys.exit(1)

# iterate through the Owners
for owner in owners:
    print(owner.id)
    print(owner.name)
    print(owner.type)
    print('')