try:
    import ConfigParser
except:
    import configparser as ConfigParser
import sys

from threatconnect import ThreatConnect

config = ConfigParser.RawConfigParser()
config.read('./tc.conf')

class owner:
    try:
        api_access_id = config.get('threatconnect', 'api_access_id')
        api_secret_key = config.get('threatconnect', 'api_secret_key')
        api_default_org = config.get('threatconnect', 'api_default_org')
        api_base_url = config.get('threatconnect', 'api_base_url')
    except ConfigParser.NoOptionError:
        print('Could not read configuration file.')
        sys.exit(1)
    tc = ThreatConnect(api_access_id, api_secret_key, api_default_org, api_base_url)
    owners = tc.owners()

    def getOwnerNames(self):
        namelist = []
        for owner in self.owners:
            namelist.append(owner.name)
        return namelist

    def getOwnerMetrics(self):
        metriclist = []
        metrics = self.owners.retrieve_metrics()
        for metric in metrics:
            metriclist.append(metric)
        return metriclist