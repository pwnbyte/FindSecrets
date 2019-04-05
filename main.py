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

## get only javascript from <script src=*
results_only_js = ks.scrapper()
ks.grabber(results_only_js)

## get javascript from <link href=*
results_link_tag = ks.scrapper_tag_link_src()
ks.grabber(results_link_tag)