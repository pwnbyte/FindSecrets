from keysniffer import KeySniffer
import argparse
import banner
from colors import bcolors

print(bcolors.GREEN + banner.banner())
parser = argparse.ArgumentParser(description="Get all sensitive information on javascript files from a give domain")
parser.add_argument("--url", required=True, help="[+] URL from a domain")
args = parser.parse_args()


url = args.url
ks = KeySniffer(args.url)
ks.verify_url()


## get only javascript from <script src=* and return array of urls
results_js = ks.scrapper() 
ks.grabber(results_js)
