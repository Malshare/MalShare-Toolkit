#! /usr/bin/env python
# Download files with given hashes.json file

import argparse
import json
import logging
import os
import sys
from multiprocessing.pool import Pool

import requests
import tqdm

api_key = "<API_KEY>"

logging.basicConfig(format = '%(asctime)s %(levelname)s:%(message)s', level = logging.INFO)


def download_file_by_hash(file_hash):
    logging.debug("Downloading {}".format(file_hash))
    try:
        malshare_url = "http://malshare.com/sampleshare.php"
        payload = {'action': 'getfile', 'api_key': api_key, 'hash': file_hash}
        user_agent = {'User-agent': 'wget_malshare daily 1.0'}

        r = requests.get(malshare_url, params = payload, headers = user_agent)
        sample = r.content

        if sample == "Sample not found":
            logging.error("Sample not Found")
            return None
        if sample == "ERROR! => Account not activated":
            logging.error("Bad API Key")
            return None

        with open(os.path.join("files", file_hash), mode = "wb") as fh:
            fh.write(sample)
            logging.info("{} saved to files".format(file_hash))

    except Exception as e:
        logging.error("download_file_by_hash: Problem connecting. Please Try again.")
        logging.exception(sys.exc_info())
        logging.exception(type(e))
        logging.exception(e.args)
        logging.exception(e)
        sys.exit(1)


def download_list(hash_list):
    files = json.load(open(hash_list))
    pool = Pool(os.cpu_count())
    for _ in tqdm.tqdm(pool.imap_unordered(download_file_by_hash, files), total = len(files)):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--apikey", help = "API Key", required = False)
    parser.add_argument("-f", "--hash_list", help = "File containing list of hashes in json format", required = True)
    args = parser.parse_args()
    global api_key
    if args.apikey:
        api_key = args.apikey
    download_list(args.hash_list)
