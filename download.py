# -*- coding: utf-8 -*-
"""
1. A small script I can run in a cronjob every 5 minutes to fetch the latest
exchange rate from here: https://openexchangerates.org/documentation

Here is the URL to fetch the json exchange rate from:
https://openexchangerates.org/api/latest.json?app_id=732ffe84fbe349b28d77b5f3c5f03aac

    $ python static_script_exchange_rate_download.py /var/www/html/aux-files-static-operation/static-scripts/scripts-site-files/exchange_rate.json 56f59d881c1a426fbbbc04d55fac52e1
"""
from argparse import ArgumentParser
from decimal import Decimal
import json

from openexchangerates import OpenExchangeRatesClient


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(JSONEncoder, self).default(o)


def interface(output_file, openexchangerates_api_key, currency):
    client = OpenExchangeRatesClient(openexchangerates_api_key)
    currencies = client.latest(base=currency)
    with open(output_file, 'wb') as f:
        json.dump(currencies, f, cls=JSONEncoder)
    print "DONE"

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("output_file")
    parser.add_argument("api_key")
    parser.add_argument("-c", "--currency", dest="currency", default="USD")

    args = parser.parse_args()

    interface(args.output_file, args.api_key, args.currency)
