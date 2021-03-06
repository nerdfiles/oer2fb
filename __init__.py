# -*- coding: utf-8 -*-

"""
    $ python __init__.py --firebase-space https://exrates-<some_id>.firebaseio.com --firebase-path currencies --openexchangerates-key <api_key>
"""

from argparse import ArgumentParser
from open_exchange_rates.client import Client
from firebase import firebase
from decimal import Decimal
import os
import json
import jwt
import Crypto.PublicKey.RSA as RSA
import datetime


class JSONEncoder(json.JSONEncoder):
    """
    @name JSONEncoder
    @description
    """

    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(JSONEncoder, self).default(o)


def load_service_account():
  with open('service-account.json') as f:
    file_contents = json.load(f)
  return file_contents


def load_private_key():
  with open('exrates-a6f3b089b509.json') as f:
    file_contents = json.load(f)
    return file_contents


def create_custom_token(uid, is_premium_account):

  try:
    secret = load_private_key()
  except Exception as e:
    print "Error loading private key: " + e.message

  try:
    sa = load_service_account()
  except Exception as e:
    print "Error loading account data: " + e.message

  try:
    payload = {
      "iss": sa['email'],
      "sub": sa['email'],
      "aud": "https://identitytoolkit.googleapis.com/google.identity.identitytoolkit.v1.IdentityToolkit",
      "uid": uid,
      "claims": {
        "premium_account": is_premium_account
      }
    }
    exp = datetime.timedelta(minutes=60)
    return jwt.encode(payload, secret, algorithm="RS256")
  except Exception as e:
    print "Error creating custom token: " + e.message
    return None


def currencies(openexchangerates_api_key, currency):
    """
    @name currencies
    @description
    @usage
    currencies(api_key, currency)
    """

    client = Client(app_id=openexchangerates_api_key)
    latest_for_currency = client.get_latest_for_currency(currency)
    return json.dumps(latest_for_currency, cls=JSONEncoder)


def interface(firebase_space, firebase_path, firebase_index_path, firebase_counter_path, openexchangerates_key):
    """
    @name interface
    @description
    """

    data = currencies(openexchangerates_key, 'USD')

    # counter_path, counter_key = os.path.split(firebase_counter_path)
    # fb.put(counter_path,
    #         counter_key,
    #         len(data))

    try:
      p = create_custom_token('<email>@gmail.com', False)
    except Exception as e:
      print "Unable to create token"

    try:
      # fb = firebase.FirebaseApplication(firebase_space, authentication=p)
      fb = firebase.FirebaseApplication(firebase_space, None)
      # fb.put(firebase_path, firebase_index_path, data)
    except Exception as e:
      print "Error writing to Firebase: " + e.message
      return None


if __name__ == "__main__":
    """
    @description
    Main CLI
    """

    parser = ArgumentParser()
    parser.add_argument("-fs", "--firebase-space", dest="firebase_space",
                        default='https://exrates.firebaseio.com')
    parser.add_argument("-fp", "--firebase-path", dest="firebase_path",
                        default='currencies')
    parser.add_argument("-fpi", "--firebase-index-path",
                        dest="firebase_index_path", default='path_id')
    parser.add_argument("-fpc", "--firebase-counter-path",
                        dest="firebase_counter_path", default='counter_id')
    parser.add_argument("-oek", "--openexchangerates-key",
                        dest="openexchangerates_api_key")
    args = parser.parse_args()

    interface(args.firebase_space,
            args.firebase_path,
            args.firebase_index_path,
            args.firebase_counter_path,
            args.openexchangerates_api_key)

