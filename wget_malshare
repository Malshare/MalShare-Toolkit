#! /usr/bin/env python
# Copyright (C) 2013 - 2016 Malshare Developers.
# Pull sample by [MD5 | SHA1 | SHA256] Hash

import os
import re
import sys
import logging
import requests
import argparse

api_key =""

def main():
    global api_key

    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--apikey", help="API Key", required=False)
    parser.add_argument("-d", "--download", help="Search / Download Hash", required=True)
    parser.add_argument("-x", "--vxcage", help="VXCage server", required=False)

    args = parser.parse_args()
    if stored_api_check() == False:
        if args.apikey:
            api_key = args.apikey

    if (not api_key):
        logging.error("API Key not entered")
        sys.exit(1)
    
    pull_file(args.download, args.vxcage, api_key )
    
def pull_file(file_hash, vxcage, api_key):
    try:
     malshare_url = "http://api.malshare.com/sampleshare.php"
     payload = {'action': 'getfile', 'api_key': api_key, 'hash' : file_hash }
     user_agent = {'User-agent': 'wget_malshare daily 1.0'}

     r = requests.get(malshare_url, params=payload, headers=user_agent)

     sample = r.content

     if (sample == "Sample not found"):
         logging.error("Sample not Found")
         return None
     if (sample == "ERROR! => Account not activated"):
         logging.error("Bad API Key")
         return None
     open(os.path.join(file_hash),"wb").write(sample)
     logging.info("Saved %s" % file_hash)

     if vxcage:
         vxcage_url = vxcage + "/malware/add"
         files = {'file': sample }
         payload = {'tags' : 'malshare'}
         r = requests.post(vxcage_url, files=files, data=payload, headers=user_agent)
         if r.json()['message'] == 'added':
             logging.info("Uploaded %s to VXCage" % file_hash)
    except Exception as e:
        logging.error("Problem connecting. Please Try again.")
        logging.exception(sys.exc_info())
        logging.exception(type(e))
        logging.exception(e.args)
        logging.exception(e)
        sys.exit(1)

# Read ~/.malshare and read the first line.  This file only needs the API string in it.
def stored_api_check():
    global api_key
    try:
        if ( os.path.exists(os.path.expanduser('~') + '/.malshare' ) ): 
            with open( os.path.expanduser('~') + '/.malshare' ) as handle_api_file:
                api_key = func_parse_api_key(handle_api_file.readlines())
		return True
        elif (  os.path.exists('.malshare' ) ): 
            with open( '.malshare' ) as handle_api_file:
                api_key = func_parse_api_key(handle_api_file.readlines())
		return True
    except IOError:
        pass
    return False

# Parse the API key and exit if the API key contains any non [A-Za-z0-9]+
def func_parse_api_key(lst_tmp_key):
    str_tmp_key = "".join(lst_tmp_key).rstrip()
    if re.match("^[A-Za-z0-9]+$", str_tmp_key): 
        return str_tmp_key



if __name__ == "__main__":
    main()
    
