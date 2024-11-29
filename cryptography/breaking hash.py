#!/usr/bin/env python3

import re
import os
import requests
import argparse
import concurrent.futures
import subprocess
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Hash cracking tool')
    parser.add_argument('-s', help='hash', dest='hash')
    parser.add_argument('-f', help='file containing hashes', dest='file')
    parser.add_argument('-d', help='directory containing hashes', dest='dir')
    parser.add_argument('-t', help='number of threads', dest='threads', type=int, default=4)
    parser.add_argument('-o', help='output file', dest='output', default='cracked_hashes.txt')
    return parser.parse_args()

def gamma(hashvalue):
    try:
        response = requests.get(f'https://www.nitrxgen.net/md5db/{hashvalue}', timeout=5)
        response.raise_for_status()
        return response.text if response.text else False
    except requests.RequestException as e:
        logger.error(f'Error in gamma function: {e}')
        return False

def theta(hashvalue):
    try:
        url = f'https://md5decrypt.net/Api/api.php?hash={hashvalue}&hash_type=md5&email=deanna_abshire@proxymail.eu&code=1152464b80a61728'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text if response.text else False
    except requests.RequestException as e:
        logger.error(f'Error in theta function: {e}')
        return False

def crack(hashvalue):
    if len(hashvalue) == 32:
        for func in [gamma, theta]:
            r = func(hashvalue)
            if r:
                return r
    return False

def threaded(hashvalue):
    resp = crack(hashvalue)
    if resp:
        return f'{hashvalue}:{resp}'
    return None

def grepper(directory):
    try:
        output = subprocess.check_output(
            f'grep -Pr "[a-f0-9]{{32}}" {directory} --exclude=*.{{png,jpg,jpeg,mp3,mp4,zip,gz}} | grep -Po "[a-f0-9]{{32}}"',
            shell=True, text=True)
        output_file = f'{os.getcwd()}/{os.path.basename(directory)}.txt'
        with open(output_file, 'w') as f:
            f.write(output)
        logger.info(f'Results saved in {output_file}')
        return set(output.split())
    except subprocess.CalledProcessError as e:
        logger.error(f'Error during grep: {e}')
        return set()

def miner(file):
    found = set()
    try:
        with open(file, 'r') as f:
            for line in f:
                found.update(re.findall(r'[a-f0-9]{32}', line))
    except IOError as e:
        logger.error(f'Error reading file: {e}')
    return found

def process_hashes(hashes, thread_count):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = {executor.submit(threaded, hash): hash for hash in hashes}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(hashes), desc="Cracking hashes"):
            result = future.result()
            if result:
                results.append(result)
    return results

def save_results(results, output_file):
    with open(output_file, 'w') as f:
        for result in results:
            f.write(f'{result}\n')
    logger.info(f'Results saved in {output_file}')

def main():
    args = parse_arguments()
    
    print('''
    M   M  OOO  H   H  AAAAA  M   M  M   M  EEEEE  DDDD
    MM MM O   O H   H A     A MM MM MM MM E     E D   D
    M M M O   O HHHHH AAAAAAA M M M M M M EEEEE   D   D
    M   M O   O H   H A     A M   M M   M E       D   D
    M   M  OOO  H   H A     A M   M M   M EEEEE   DDDD 
    ''')

    if args.dir:
        hashes = grepper(args.dir)
    elif args.file:
        hashes = miner(args.file)
    elif args.hash:
        result = crack(args.hash)
        if result:
            print(f'{args.hash}:{result}')
        else:
            print('Hash was not found in any database.')
        return
    else:
        logger.error('Please provide a hash, file, or directory to process.')
        return

    if hashes:
        logger.info(f'Hashes found: {len(hashes)}')
        results = process_hashes(hashes, args.threads)
        save_results(results, args.output)
    else:
        logger.warning('No hashes found to process.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('\nOperation interrupted by user.')
    except Exception as e:
        logger.exception(f'An unexpected error occurred: {e}')
