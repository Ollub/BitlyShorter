import os
import logging
import argparse

import requests
from dotenv import load_dotenv

api_key = os.getenv("API_KEY")

logger = logging.getLogger('bitly_helper')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('bitly.log')
formatter = logging.Formatter('%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)



def get_short_link(long_url=None, api_key=None):
    '''
    creating bitling from long url.

    PARAMS:
        long_url: url that should be shorten
        api_key: bit.ly api_key
    RETURN: bitlink or provides error to external code
            by using response.raise_for_status
    '''
    url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {"Authorization": "Bearer {}".format(api_key)}
    payload = {'long_url': '{}'.format(long_url),
               'domain': "bit.ly",
           }
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
    return r.json()['link']


def check_bitlink(bitlink=None, api_key=None):
    '''
    checks if provided bitlink is correct

    PARAMS:
        bitlink: bitlink
        api_key: bit.ly api_key
    RETURN: NONE or provides error to external code
            by using response.raise_for_status
    '''
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {"Authorization": "Bearer {}".format(api_key)}
    r = requests.get(url, headers=headers)
    r.raise_for_status()


def get_click_info(bitlink=None, api_key=None, unit='day', units=-1):
    '''
    returns number of clicks for provided bitlink
    
    PARAMS:
        bitlink: bitlink
        api_key: bit.ly api_key
        unit: day, minute, hour, week, month
        units: number of units or all if -1
    RETURN: umber of clicks for provided bitlink or 
            provides error to external code
            by using response.raise_for_status
    '''
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {"Authorization": "Bearer {}".format(api_key)}
    payload = {
        'unit': unit,
        'units': units        
              }
    r = requests.get(url, headers=headers, params=payload)
    r.raise_for_status()
    return r.json()['total_clicks']


def main(link=None, api_key=None):
    '''
    if bitlink provided prints clicks information
    if long url provided prints short link
    '''
    logger.info('Program started')
    load_dotenv()
    if not api_key:
        print('Please provide api key to main function')
        logger.error('api_key was not provided')
        return None

    if not link:
        parser = argparse.ArgumentParser()
        parser.add_argument('-l', '--link', help='bitlink or long url')
        args = parser.parse_args()
        link = args.link
    if not link:
        link = input('Please enter your link: ')

    logger.info('Provided link: {}'.format(link))

    try:
        check_bitlink(link, api_key)
        clicks = get_click_info(link, api_key)
        logger.info('Bitlink correct. End \n')
        print('Your bitlink was clicked {} times'.format(clicks))
        return None
    except requests.exceptions.HTTPError as err:
        logger.warning('Bitlink checked unsuccessfully. HTTP error: {}'.format(err))
    try:
        bitlink = get_short_link(link, api_key)
        print('You have created shorten link: {}'.format(bitlink))
        logger.info('Bitlink was created succesfully')
    except requests.exceptions.HTTPError as err:
        logger.error('Provided link or api_key is not correct. HTTP error: {}'.format(err))
        print('Provided link or api_key is not correct')


if __name__ == '__main__':
    main(link=None, api_key=api_key)