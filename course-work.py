import json
import argparse
import requests
from datetime import datetime


# take arguments from command line
def pars():
    parser = argparse.ArgumentParser()
    parser.add_argument('currency')
    parser.add_argument('date', nargs='?', default=datetime.now().strftime("%Y%m%d"))
    return parser.parse_args()


# convert currency to upper case
currency = pars().currency.upper()
# format the date in the desired format, if the user entered an arbitrary date
date = "".join([x for x in pars().date if x.isdigit()])
# make a request for a resource using the date from the parser
request = json.loads(
    requests.get(f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={date}&json").content)


def rate(curr):
    # check the date, if the date is not correct, the length of the list request, will be less than 2
    if len(request) < 2:
        return print(f"Invalid date {pars().date}")
    # check the currency, according to the standard it is three letters
    if len(curr) != 3 or not curr.isalpha():
        return print("System Error")
    # check the availability of currency on the resource
    for x in request:
        if curr == x['cc']:
            return print(x['cc'], x['rate'], sep="\n\n")
    # Currency not found on resource, return Invalid currency name
    return print(f"Invalid currency name: {curr}")


rate(currency)
