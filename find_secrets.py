#!/usr/bin/python3

import requests
import argparse
import os
import sys
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

__AUTHOR__ = 'Gh0sTNiL'
__VERSION__ = 'v01.BETA'




## MENU
parser = argparse.ArgumentParser(description='Tool to find secrets on input domain')
parser.add_argument('-u', '--url', type=str, required=True, help="[+] URL for crawler")
parser.add_argument('--random_agent', type=str, help="Random user agents")
args = parser.parse_args()
url = args.url

if 'http://' not in url and 'https://' not in url:
    print("[-] Provide a schema http:// or https:// for {}".format(url))
    sys.exit()



REGEX_PATTERN = {"Api": "/api", "AmazonEndPoint": 'https?:\/\/(.*).amazonaws.com', "AcessKeyAws": "ACCESS_KEY_ID", "SecretKeyAws": "SECRET_KEY",
"Authorization": "Authorization", "appToken": "appToken", "appKey":"appKey"}
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/70.0.3538.77 Chrome/70.0.3538.77 Safari/537.36"}





def banner():

    p = ''' 
    {}:{}
#######                  #####                                           
#       # #    # #####  #     # ######  ####  #####  ###### #####  ####  
#       # ##   # #    # #       #      #    # #    # #        #   #      
#####   # # #  # #    #  #####  #####  #      #    # #####    #    ####  
#       # #  # # #    #       # #      #      #####  #        #        # 
#       # #   ## #    # #     # #      #    # #   #  #        #   #    # 
#       # #    # #####   #####  ######  ####  #    # ######   #    ####  
     '''
    return p.format(__AUTHOR__, __VERSION__)



def send_requests(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
        if r.status_code != 404:
            crawler_js(r.text, url)
    except requests.exceptions.Timeout as e:
        print("[+] Timeout Error for {}".format(e))
        pass
    except requests.exceptions.MissingSchema as e:
        print("[+] Missing Schema https:// or http:// for {}".format(url))
        pass
    except requests.exceptions.TooManyRedirects as e:
        print("[+] Too many redirects found for {}".format(url))
        pass


def parser_js_endpoints(src_tag, url):
    # return a domain from URL passed
    domain_path = urlparse(src_tag)
    # print(domain_path.netloc)

    if domain_path.netloc == '':
        return url + src_tag
    elif domain_path.netloc != url:
        return src_tag
    else:
        return url + src_tag    
    
    



def crawler_js(requests_objt, url):
    # pattern = re.compile(r'src=(.*)"')
    soup = BeautifulSoup(requests_objt, 'html.parser')
    src_tags_list = []
    for script_tag in soup.find_all('script'):
        if script_tag:
            src_tags_list.append(script_tag.get('src'))
    
    # Remove None elements from 
    filter_src_tag_list = [ src_js for src_js in src_tags_list if src_js is not None]
    
    # Concat js with domain crawled
    for endpoint_js in filter_src_tag_list:
        parsed_endpoint = parser_js_endpoints(endpoint_js, url)
        print(parsed_endpoint)
        
    

if __name__ == "__main__":
    print(banner())
    send_requests(url)
