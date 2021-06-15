import configparser as ConfigParser
import sys
import pandas as pd
import os

import owners
import util

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

    f_name_directory = os.getcwd() + r"\csv"
    n_files = len(os.listdir(f_name_directory))
    filename = os.path.join(f_name_directory, "{}.csv".format(n_files))

    def format(self, indicators):
        col = self.pcol
        try:
            for indicator in indicators:
                tagname = ""
                #value = ""
                indicator.load_attributes()
                indicator.load_tags()

                col["Indicator"].append(indicator.indicator)
                col["Type"].append(indicator.type)
                col["Organization"].append(indicator.owner_name)
                col["Rating"].append(indicator.rating)
                col["Confidence"].append(indicator.confidence)
                col["DateAdded"].append(indicator.date_added)
                col["Description"].append(indicator.description) if len(indicator.description) > 0 or indicator.description != None else "0"
                col["Source"].append(indicator.source) if len(indicator.source) > 0 or indicator.description != None else "0"

                if len(indicator.tags) > 0:
                    for tag in indicator.tags:
                        tagname += tag.name + ";"
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

    def tocsv(self, data):
        try:
            df = pd.DataFrame(data)
            df.to_csv(self.filename)
        except Exception as exception:
            assert exception.__class__.__name__ == "NameError"