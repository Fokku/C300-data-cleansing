import pycountry
import tocsv
import re

"""
csv = tocsv()
c_names = [country.name for country in pycountry.countries]
c_alpha2 = [country.alpha_2 for country in pycountry.countries]
c_alpha3 = [country.alpha_3 for country in pycountry.countries]

c_alpha4 = [country.alpha_4 for country in pycountry.historic_countries]
"""

print("kk")
txt = "Country: DC"
x = re.search("(Country)\W\s\w\w", txt)
print(x)
if x:
    print("ey")
