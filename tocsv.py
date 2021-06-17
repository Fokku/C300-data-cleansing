import configparser as ConfigParser
import sys
import pandas as pd
import os
from datetime import datetime
import time

import owners
import datacleansing as dtc

class csv:

    pcol = {
        "Indicator": [],
        "Type": [],
        #"Value": [],
        "Organization": [],
        "Rating": [],
        "Confidence": [],
        "DateAdded": [],
        #"LastModified": [],
        "Description": [],
        "Source": [],
        # TODO IN CASE MENG HONG NEEDS IT
        # "DNS": [],
        # "Whois": [],
        # "Active": [],
        # "Observations": [],
        # "Date Last Observed": [],
        # "False Positives": [],
        # "Date FP Last Reported": [],
        "Tags": []
    }

    dc = dtc.dataCleanse()
    now = datetime.now()

    log_directory = os.getcwd() + r"\log"
    log_filename = os.path.join(log_directory, "{}.csv".format(now.strftime("%Y%m%dT%H%M%S")))

    def format(self, indicators):
        col = self.pcol
        try:
            for indicator in indicators:
                tagname = ""
                # value = ""
                indicator.load_attributes()
                indicator.load_tags()

                col["Indicator"].append(indicator.indicator)
                col["Type"].append(indicator.type)
                col["Organization"].append(indicator.owner_name)
                col["Rating"].append(indicator.rating)
                col["Confidence"].append(indicator.confidence)
                col["DateAdded"].append(indicator.date_added)
                col["Description"].append(indicator.description if not self.dc.checkForEmptyValues(indicator.description) else "0")
                col["Source"].append(indicator.source if not self.dc.checkForEmptyValues(indicator.source) else "0")

                if len(indicator.tags) > 0:
                    for tag in indicator.tags:
                        if pd.notna(tag):
                            c_type = self.dc.checkCountryCodeType(tag.name)
                            if bool(c_type):
                                tagname = self.dc.convertToCountryObject(tag=tag.name, type=c_type).name
                            else:
                                tagname = tag.name
                        else:
                            tagname = ""
                        tagname += ";"
                else:
                    tagname = "0"
                col["Tags"].append(tagname)
                """
                for attr_obj in indicator.attributes:
                    value += attr_obj.value + ";"
                    col["LastModified"].append(attr_obj.last_modified)
                col["Value"].append(value)
                """
            return col
        except Exception as exception:
            assert exception.__class__.__name__ == "NameError"

    def tocsv(self, data, directory, logging=True):
        try:
            df = pd.DataFrame.from_dict(data, orient='columns', columns=None)
            df.to_csv(directory)
            time.sleep(5)
            if logging:
                df.to_csv(self.log_filename)
        except Exception as exception:
            assert exception.__class__.__name__ == "NameError"
