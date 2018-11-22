#!/usr/bin/python3


import requests
import random
import argparse
import os
import sys
import re, fnmatch
import glob
import datetime, time
import shutil
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import colors


__AUTHOR__ = 'Gh0sTNiL'
__VERSION__ = 'v01.BETA'


## GLOBAL VARS
global agent
global dirname
dirname = ''
agent = ''

## REGEX PATTERN
REGEX_PATTERN = {"Api": '[A-Za-z0-9\._+]*\/api\/[A-Za-z0-9\._+]*', 
"AmazonEndPoint": 'https:\/\/[A-Za-z0-9\-.*]*.amazonaws.com', 
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



# create a dir with name of target name
dirname = urlparse(url).netloc


try:
    os.mkdir(dirname)
    print(colors.Color.OKBLUE + "[*] Created a DIR with name {}".format(dirname))
    print(colors.Color.END)
except FileExistsError as e:
    print(colors.Color.FAIL + "[-] File Exists {} Would u like to overwrite {} y/n".format(dirname,dirname))
    print(colors.Color.END)
    c = input()
    if len(c) == 1 and c.lower() == 'y':
        shutil.rmtree(dirname)
        os.mkdir(dirname)
    else:
        print(colors.Color.FAIL + "[*] Delete manually and try again ;)")
        print(colors.Color.END)
        sys.exit()


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
        r = requests.get(url, headers=HEADERS, timeout=5, allow_redirects=True)
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
    except requests.exceptions.RetryError as e:
        print("[+] Redirect Error for {}".format(url))
    


def parser_js_endpoints(src_tag, url):
    # return a domain from URL passed
    domain_path = urlparse(src_tag)
    

    if domain_path.netloc == '':
        return url + src_tag
    elif domain_path.netloc != url:
        if src_tag[:2] == '//':
            new_src_tag = src_tag.replace('//', 'https://')
            return new_src_tag
        return src_tag
    else:
        return url + src_tag    
    


def save_jsEnpoint_file(js_endpoint):

    parsed_endpoint_name_https = js_endpoint.replace('https://', '_')
    parsed_endpoint_name_slash = parsed_endpoint_name_https.replace('/','_')
    parsed_endpoint_name_txt = parsed_endpoint_name_slash.replace('.js', '.txt')

    ## parse URL when the length is higher than 150 to save with the name
    if len(parsed_endpoint_name_txt) > 150:
        parsed_endpoint_name_txt = parsed_endpoint_name_txt.split('?')[0]

    fullpath = os.path.join(dirname, parsed_endpoint_name_txt)


    try:
        r = requests.get(js_endpoint, headers=HEADERS, timeout=5)
        if r.status_code != 404:
            with open(fullpath, 'wb') as f:
                f.write(r.content)
            f.close()

    except requests.exceptions.Timeout as e:
        print("[+] Timeout Error for {}".format(e))
        pass
    except requests.exceptions.MissingSchema as e:
        print("[+] Missing Schema https:// or http:// for {}".format(url))
        pass
    except requests.exceptions.TooManyRedirects as e:
        print("[+] Too many redirects found for {}".format(url))
        pass

    
def grab_patterns_from_js(regex_pattern_hash):
    #api = re.findall(regex_pattern_hash['Api'], text)
    #amazonaws = re.findall(regex_pattern_hash['AmazonEndPoint'], text)

    for filepath in glob.glob(os.path.join(dirname, '*.txt')):
        with open(filepath, errors='ignore') as f:
            content = f.read()
            api = re.findall(regex_pattern_hash['Api'], content)
            amazonaws = re.findall(regex_pattern_hash['AmazonEndPoint'], content)
            AcessKeyAws = re.findall(regex_pattern_hash['AcessKeyAws'], content)
            SecretKeyAws = re.findall(regex_pattern_hash['SecretKeyAws'], content)
            Authorization = re.findall(regex_pattern_hash['Authorization'], content)



            if api:
                print(api)
            if amazonaws:
                print(amazonaws)
            if AcessKeyAws:
                print(colors.Color.OKGREEN + "[*] Possible access key found")
            if SecretKeyAws:
                print(colors.Color.OKGREEN + "[*] Possible secret key found on")
            if Authorization:
                print(colors.Color.OKGREEN + "[*] Possible authorization key found on")

            




def crawler_js(requests_objt, url):
    
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
        save_jsEnpoint_file(parsed_endpoint)

    print(colors.Color.OKGREEN + "[*] Crawler end, total scripts founded! {}".format(len(filter_src_tag_list)))
    print(colors.Color.OKGREEN + "[*] All scripts were saved on dir called {} !".format(dirname))
    print(colors.Color.END)       
    

if __name__ == "__main__":
    print(colors.Color.WARNING +banner() + colors.Color.END)
    send_requests(url)
    grab_patterns_from_js(REGEX_PATTERN)
