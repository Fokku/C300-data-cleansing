import pandas as pd
import numpy as np
import pycountry
import re

class dataCleanse:
    c_names = [country.name for country in pycountry.countries]
    c_alpha2 = [country.alpha_2 for country in pycountry.countries]
    c_alpha3 = [country.alpha_3 for country in pycountry.countries]

    def checkCountryCodeType(self, tag):
        if tag in self.c_alpha2:
            return "Alpha 2"
        elif tag in self.c_alpha3:
            return "Alpha 3"
        else:
            return False

    def convertToCountryObject(self, tag, type):
        print(tag)
        if type == "Alpha 2":
            return pycountry.countries.get(alpha_2=tag)
        elif type == "Alpha 3":
            return pycountry.countries.get(alpha_3=tag)

    def checkForEmptyValues(self, value):
        if pd.notna(value):
            if len(value) > 0:
                return False
            else:
                return True
        else:
            return True
