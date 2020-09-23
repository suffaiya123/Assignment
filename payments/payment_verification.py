from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlencode
from hashlib import sha512
from uuid import uuid4
from random import randint
import urllib.request as urllib2
import json
import random
from datetime import datetime
import hashlib, logging, traceback
from Paymenypayfort import settings

from .payment_gateway_constants import (MERCHANT_IDENTIFIER,
                                        MERCHANT_REFERENCE)
# define your code here.

KEYS = ('txnid', 'amount', 'productinfo', 'firstname', 'email',
        'udf1', 'udf2', 'udf3', 'udf4', 'udf5', 'udf6', 'udf7', 'udf8',
        'udf9', 'udf10')

Webservicekeys = ('key', 'command', 'var1')


# generate the hash
def generate_hash(data):
    try:
        # get keys and SALT from dashboard once account is created.
        # hashSequence = "key|txnid|amount|productinfo|firstname|email|
        # udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = get_hash_string(data)
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        return generated_hash
    except Exception as e:
        # log the error here.
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


# create hash string using all the fields

def get_hash_string(data):
    hashSequence = "txnid|amount|productinfo|firstname|" \
                   "email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
    hash_string = "KBz6jjfg|"
    hashVarsSeq = hashSequence.split('|')
    for i in hashVarsSeq:
        try:
            hash_string += str(data[i])
        except Exception:
            hash_string += ''
        hash_string += '|'
    hash_string += "WQdQk2jvY7"
    return hash_string


def get_reverse_hash_string(data):
    hashSequence = "status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|txnid"
    hash_string = "WQdQk2jvY7|"
    data.update({'status': 'User Cancelled'})
    hashVarsSeq = hashSequence.split('|')
    for i in hashVarsSeq:
        try:
            hash_string += str(data[i])
        except Exception:
            hash_string += ''
        hash_string += '|'
    hash_string += "KBz6jjfg"
    return hash_string


def generate_response_hash(data):
    data.update({'salt': 'WQdQk2jvY7',
                'key': 'KBz6jjfg'})
    print(data)
    try:
        additionalCharges = data["additionalCharges"]
        if additionalCharges != '' and ((additionalCharges != 0.00 or additionalCharges !=0.0)
                                        or (additionalCharges != '0.00' or additionalCharges != '0.0')):
            retHashSeq = additionalCharges + '|' + data['salt'] + '|' + data['status'] + '|||||||||||' + data[
                'email'] + '|' \
                         + data['firstname'] + '|' + data['productinfo'] + '|' + data['amount'] + '|' + data[
                             'txnid'] + '|' + data['key']
        else:
            retHashSeq = data['salt'] + '|' + data['status'] + '|||||||||||' + data['email'] + '|' \
                         + data['firstname'] + '|' + data['productinfo'] + '|' + data['amount'] + '|' + data[
                             'txnid'] + '|' + data['key']
    except Exception:
        retHashSeq = data['salt'] + '|' + data['status'] + '|||||||||||' + data['email'] + '|' \
                     + data['firstname'] + '|' + data['productinfo'] + '|' + data['amount'] + '|' + data[
                         'txnid'] + '|' + data['key']
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    return hashh


# generate a random transaction Id.
def get_transaction_id():
    random.seed(datetime.now())
    hash_object = hashlib.sha512(str(random.random()).encode("utf-8"))
    # hash_object = hashlib.sha512(str(randint(0, 9999)).encode("utf-8"))
    # take appropriate length
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid
