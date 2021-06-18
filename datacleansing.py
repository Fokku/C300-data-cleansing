import pandas as pd
import numpy as np
import pycountry
import re

class dataCleanse:
    c_names = [country.name for country in pycountry.countries]
    c_alpha2 = [country.alpha_2 for country in pycountry.countries]
    c_alpha3 = [country.alpha_3 for country in pycountry.countries]

    def checkCountryCodeType(self, tag):
        if tag in self.c_alpha2 or re.search(r"(Country)\W\s\w\w", tag):
            return "Alpha 2"
        elif tag in self.c_alpha3 or re.search(r"(Country)\W\s\w\w", tag):
            return "Alpha 3"
        else:
            return False

    def convertToCountryObject(self, tag, t_type):
        try:
            if t_type == "Alpha 2":
                for code in self.c_alpha2:
                    if re.search(code, tag):
                        return pycountry.countries.get(alpha_2=code)
            elif t_type == "Alpha 3":
                for code in self.c_alpha3:
                    if re.search(code, tag):
                        return pycountry.countries.get(alpha_3=code)
        except:
            raise Exception("convertToCountryObject fed invalid tag (Not an alpha_2 or alpha_3 country code")

    def checkForEmptyValues(self, value):
        if pd.notna(value):
            if len(value) > 0:
                return False
            else:
                return True
        else:
            return True
