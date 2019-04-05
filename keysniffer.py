#/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re
from colors import bcolors

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


#TODO
#<script type="text/javascript" src=""></script>


__AUTHOR__ = "gh0stN1L"
__VERSION__ = "1.0"
headers = {"User-agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)"}


def parser_regex(matchregex):
        matchregex = set(matchregex)
        for mtch in matchregex:
            return mtch


class KeySniffer:

    def __init__(self, url):
        self.url = url
        
          
    def verify_url(self):
        if self.url == "":
            print("[+] Usage: python3 main.py --url https://domain.py")
        schema = urlparse(self.url)
        if schema.scheme == "":
            print("[-] U dont pass a scheme.. all requests will be made with https://")
            self.url = "https://" + self.url
            print(self.url)


    
    def scrapper(self):
        array_urrls = []
        try:
            r = requests.get(self.url,headers=headers,timeout=5.0)
            text = r.text
            print(bcolors.RED + "[*] Starting search for scripts tags...")
            print(bcolors.VIOLET + "[+] status code: for {} --> [{}]".format(self.url,r.status_code))
            print("\n\n")
        except (Exception,requests.exceptions.Timeout) as e:
            print(e)

        bs_objt = BeautifulSoup(text,features="lxml")
        for js in bs_objt.findAll("script",{"src":re.compile("/|//|http|https")}):
            if js["src"][0:1] == "/":
                array_urrls.append(self.url + js["src"])
            elif js["src"][0:2] == "//":
                array_urrls.append(self.url + js["src"])
            else:
                array_urrls.append(js["src"])
            
        if len(array_urrls) <= 0:
            print(bcolors.RED + "[-] No javascripts found")
        else:
            print(bcolors.GREEN + "[+] Found {} POINTS with Javascript !!".format(len(array_urrls)))
            print("\n\n")

        return set(array_urrls)

    
    ## when the site uses frameworks like nextjs js are set on link tags
    def scrapper_tag_link_src(self):
        urls = set()
        
        try:
            r = requests.get(self.url,headers=headers,timeout=3.0)
            text = r.text
            print(bcolors.RED + "[*] Starting search for <link tags>...")
            print(bcolors.VIOLET + "[+] status code: for {} --> [{}]".format(self.url,r.status_code))
            print("\n\n")
        except (Exception,requests.exceptions.Timeout) as e:
            print(e)
        
        bs_objt = BeautifulSoup(text,'html.parser')
        for link in bs_objt.findAll("link"):
            if "href" in link.attrs:
                if ".js" in link.attrs:
                    print("DEBBUGER", link.attrs['js'])
                    urls.add(self.url+link.attrs["href"])
        
        if len(urls) <= 0:
            print(bcolors.WARD + "[-] No Link tags were found")
            print("\n\n")
        else:
            print(bcolors.RED + "[*] Link tags were found total: {}".format(len(urls)))
            print("\n\n")

        return urls




    def grabber(self, urls):
        count = 0

        ## REGEX PATTERNS
        REGEX_PATTERN = {"Api": '/api\/[A-Za-z0-9\._+]*',
        "AmazonEndPoint": 'https:\/\/[A-Za-z0-9\-.*]*.amazonaws.com/[A-Za-z0-9\-.*]*',
        "AmazonEndPointHTTP": 'http:\/\/[A-Za-z0-9\-.*]*.amazonaws.com/[A-Za-z0-9\-.*]*',
        "AcessKeyAws": "ACCESS_KEY_ID",
        "accessKeyId": 'accessKeyId:([A-Za-z1-9]{0,30})',
        "secretAccessKey": 'secretAccessKey:([A-Za-z1-9]{0,50})',
        "SecretKeyAws": 'SECRET_KEY:([A-Za-z1-9]{0,50})',
        "Graphql": '[A-Za-z0-9\._+]*\/graphql\/[A-Za-z0-9\._+]*',
        "Authorization": "Authorization:\s[A-Za-z0-9]*\s[A-Za-z0-9]",
        "appToken": "appToken:\s([A-Za-z1-9]{0,50}",
        "apiWithSlash": '/api\/[A-Aa-z0-9]*\/[A-Aa-z0-9]*',
        "apiWithDot": '/api.[A-Za-z0-9\._+]*\/[A-Za-z0-9\._+]*\/[A-Za-z0-9\._+]*',
        "appKey":'appkey(\S[A-Za-z0-9]*)'}

        try:
            for url in urls:
                try:
                    r = requests.get(url,headers=headers,timeout=5.0)
                except (Exception,requests.exceptions.Timeout) as e:
                    print("[-] Error {}".format(e))
                    print("\n\n")
                    continue
                
                api = re.findall(REGEX_PATTERN['Api'], r.text)
                amazonaws = re.findall(REGEX_PATTERN['AmazonEndPoint'], r.text)
                amazonawshttp = re.findall(REGEX_PATTERN['AmazonEndPointHTTP'], r.text)
                AcessKeyAws = re.findall(REGEX_PATTERN['AcessKeyAws'], r.text)
                SecretKeyAws = re.findall(REGEX_PATTERN['SecretKeyAws'], r.text)
                Authorization = re.findall(REGEX_PATTERN['Authorization'], r.text)
                apiWithSlash = re.findall(REGEX_PATTERN['apiWithSlash'], r.text)
                apiWithDot = re.findall(REGEX_PATTERN['apiWithDot'], r.text)
                appKey = re.findall(REGEX_PATTERN['appKey'], r.text)
                Graphql = re.findall(REGEX_PATTERN['Graphql'], r.text)
                secretAccessKey = re.findall(REGEX_PATTERN['secretAccessKey'], r.text)
                accessKeyId = re.findall(REGEX_PATTERN['accessKeyId'], r.text)

                if api:
                    print("[*] Found API endpoints on URL:[{}] \n\n --> {}".format(url,parser_regex(api)))
                    print("\n\n")
                    count += 1
                    
                if amazonaws:
                    print("[*]Found AWS endpoints on URL:[{}] \n\n --> {}".format(url,parser_regex(amazonaws)))
                    print("\n\n")
                    count += 1
                    
                if amazonawshttp:
                    print("[*]Found AWS endpoints on URL:[{}] \n\n --> {}".format(url,parser_regex(amazonawshttp)))
                    print("\n\n")
                    count += 1
                    
                if AcessKeyAws:
                    print("[*]Found AcessKeyAws endpoints on URL:[{}] \n\n --> {}".format(url,parser_regex(AcessKeyAws)))
                    print("\n\n")
                    count += 1
                    
                if SecretKeyAws:
                    print("[*] Possible secret key found on URL:[{}] \n\n --> {}".format(url,parser_regex(SecretKeyAws)))
                    print("\n\n")
                    count += 1
                    
                if Authorization:
                    print("[*] Possible authorization key found on URL:[{}]\n\n --> {}".format(url,parser_regex(Authorization)))
                    print("\n\n")
                    count += 1

                if apiWithSlash:
                    print("[*]Found apiWithSlash endpoints on URL:[{}] \n\n --> {}".format(url,parser_regex(apiWithSlash)))
                    print("\n\n")
                    count += 1
                if apiWithDot:
                    print("[*]Found apiWithDot endpoints on URL:[{}] \n\n --> {}".format(url,parser_regex(apiWithDot)))
                    print("\n\n")
                    count += 1
                    
                if appKey:
                    print("[*]Found appKey endpoints on URL:[{}] \n\n --> {}".format(url,parser_regex(appKey)))
                    print("\n\n")
                    count += 1

                if Graphql:
                    print("[*]Found Graphql endpoints on URL:[{}] \n\n --> {}".format(url,parser_regex(Graphql)))
                    print("\n\n")
                    count += 1
                    
                if secretAccessKey:
                    print("[*]Found secretAccessKey endpoints on URL:[{}]  \n\n --> {}".format(url,parser_regex(secretAccessKey)))
                    print("\n\n")
                    count += 1
                    
                if accessKeyId:
                    print("[*]Found accessKeyId endpoints on URL:[{}] \n\n --> {}".format(url,parser_regex(accessKeyId)))
                    print("\n\n")
                    count += 1
                    
        except Exception as e:
            print(e)



    
        

