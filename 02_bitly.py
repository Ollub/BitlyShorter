import requests
import os
import logging

api_key = os.getenv("API_KEY")
logger = logging.getLogger('bitly_helper')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('bitly.log')
formatter = logging.Formatter('%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def safe_request(func):
    def wraper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as err:
            return err
    return wraper


@safe_request
def authenticate(api_key=None):
    '''user authentication at bit.ly'''
    
    url = 'https://api-ssl.bitly.com/v4/user'
    headers = {"Authorization": "Bearer {}".format(api_key)}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        print('User {} succesfully authenticated!'.format(r.json()['login']))


@safe_request
def get_short_link(long_url=None, api_key=None):
    '''
    getting bitling from long url.
    returns bitlink
    '''
    if not long_url:
        print('Pleade provide long url')
        return None
    if not api_key:
        print('Please provide api key')
        return None
    url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {"Authorization": "Bearer {}".format(api_key)}
    payload = {'long_url': '{}'.format(long_url),
               'domain': "bit.ly",
           }
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
    return r.json()['link']


# @safe_request
# def get_click_info(bitlink=None, api_key=None, unit='day', units=-1):
#     '''
#     returns number of clicks for provided bitlink
#     unit: day, minute, hour, week, month
#     units: number of units or all if -1
#     '''
#     if not bitlink:
#         print('Pleade provide bitlink')
#         return None
#     if not api_key:
#         print('Please provide api key')
#         return None
#     url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
#     headers = {"Authorization": "Bearer {}".format(api_key)}
#     payload = {
#         'unit': unit,
#         'units': units        
#               }
#     r = requests.get(url, headers=headers, params=payload)
#     r.raise_for_status()
#     return r.json()['total_clicks']

# @safe_request
# def check_bitlink(bitlink=None, api_key=None):
#     '''
#     checks if provided bitlink is correct
#     prints ok-message or provides error to
#     an external code
#     '''
#     if not bitlink:
#         print('Pleade provide bitlink')
#         return None
#     if not api_key:
#         print('Please provide api key')
#         return None
#     url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
#     headers = {"Authorization": "Bearer {}".format(api_key)}
#     r = requests.get(url, headers=headers)
#     r.raise_for_status()
#     print('You provided bitlink for {title}'.format(title = r.json()['title']))


# def main(api_key=None, link=None):
#     '''
#     if bitlink provided prints clicks information
#     if long url provided prints short link
#     '''
#     logger.info('Program started')
#     if not api_key:
#         print('Please provide api key')
#         return None

#     # THIS PART IS NOT WORKING YET    
#     # if not link:
#     #     parser = argparse.ArgumentParser()
#     #     parser.add_argument('-l', '--link', help='Bitlink or long url')
#     #     link = parser.parse_args()['link']
#     if not link:
#         link = input('Please enter your link: ')
#     try:
#         check_bitlink(link, api_key)
#         clicks = get_click_info(link, api_key)
#         print('Your bitlink was clicked {} times'.format(clicks))
#         loger.info('Done!')
#     except:
#         bitlink = get_short_link(link, api_key)
#         if bitlink:
#             print('You have created shorten link: {}'.format(bitlink))


if __name__ == '__main__':
    result = get_short_link('https://yaru', api_key)
    print(result)

    # main(api_key)