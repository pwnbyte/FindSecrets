#!/usr/bin/python3

import requests
import random
import argparse
import os
import sys
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import colors

__AUTHOR__ = 'Gh0sTNiL'
__VERSION__ = 'v01.BETA'

global agent
agent = ''





REGEX_PATTERN = {"Api": "[A-Za-z0-9\._+]*\/api\/[A-Za-z0-9\._+]*", 
"AmazonEndPoint": '(http|https):\/\/[A-Za-z0-9\._+].*amazonaws.(com)', 
"AcessKeyAws": "ACCESS_KEY_ID", 
"SecretKeyAws": "SECRET_KEY",
"Authorization": "Authorization",
 "appToken": "appToken",
 "appKey":"appKey"}



def random_mobile_agent():
    lines = open('utils/mobile_agent.txt').read().splitlines()
    line = random.choice(lines)
    return line


def random_web_agent():
    lines = open('utils/web_agent.txt').read().splitlines()
    line = random.choice(lines)
    return line


def random_game_agent():
    lines = open('utils/game_consoles.txt').read().splitlines()
    line = random.choice(lines)
    return line



## MENU
parser = argparse.ArgumentParser(description='Tool to find secrets on input domain')
parser.add_argument('-u', '--url', type=str, required=True, help="[+] URL for crawler")
parser.add_argument('--random_agent_web',help="Random user agents web", action='store_true')
parser.add_argument('--random_agent_mobile', help="Random user agents mobile", action='store_true')
parser.add_argument('--random_agent_console', help="Random user agents console", action='store_true')
args = parser.parse_args()
url = args.url
web_user_agent = args.random_agent_web
mobile_user_agent = args.random_agent_mobile
console_user_agent = args.random_agent_console



if 'http://' not in url and 'https://' not in url:
    print("[-] Provide a schema http:// or https:// for {}".format(url))
    sys.exit()

if console_user_agent:
    agent = random_game_agent()
if mobile_user_agent:
    agent = random_mobile_agent()
if web_user_agent:
    agent = random_web_agent()

if agent == '':
        agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

HEADERS = {"User-Agent": agent}



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


    print(colors.Color.OKBLUE + "[+] Random Agent set: {}\n".format(agent))
    print(colors.Color.END)


    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
        if r.status_code != 404:
            print(colors.Color.OKGREEN + "[*] Crawler start!")
            print(colors.Color.END)
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
        if src_tag[:2] == '//':
            new_src_tag = src_tag.replace('//', 'https://')
            return new_src_tag
        return src_tag
    else:
        return url + src_tag    
    
    



def crawler_js(requests_objt, url):
    # pattern = re.compile(r'src=(.*)"')
    soup = BeautifulSoup(requests_objt, 'html.parser')
    src_tags_list = []

    # verify if scripts tags with were found
    if len(soup.find_all('script')) == 0:
        print(colors.Color.FAIL + "[-] No scripts founded on this page {} \n or maybe a bug please open a issue".format(url))

    for script_tag in soup.find_all('script'):
        if script_tag:
            src_tags_list.append(script_tag.get('src'))
    
    # Remove None elements from 
    filter_src_tag_list = [ src_js for src_js in src_tags_list if src_js is not None]
    
    # Concat js with domain crawled
    print(colors.Color.OKGREEN + "[*] Scripts were founded")
    print(colors.Color.END)
    for endpoint_js in filter_src_tag_list:
        parsed_endpoint = parser_js_endpoints(endpoint_js, url)
        print(parsed_endpoint)
    print(colors.Color.OKGREEN + "[*] Crawler end, total scripts founded! {}".format(len(filter_src_tag_list)))
    print(colors.Color.END)       
    

if __name__ == "__main__":
    print(colors.Color.WARNING +banner() + colors.Color.END)

    send_requests(url)




















