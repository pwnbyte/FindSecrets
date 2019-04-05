#!/usr/bin/python3
# -*- coding: utf-8 -*-

__AUTHOR__ = "gh0stn1L"
__VERSION__ = "1.0"


def banner():
    banner = """
     

  █████▒██▓ ███▄    █ ▓█████▄   ██████ ▓█████  ▄████▄   ██▀███  ▓█████▄▄▄█████▓  ██████ 
▓██   ▒▓██▒ ██ ▀█   █ ▒██▀ ██▌▒██    ▒ ▓█   ▀ ▒██▀ ▀█  ▓██ ▒ ██▒▓█   ▀▓  ██▒ ▓▒▒██    ▒ 
▒████ ░▒██▒▓██  ▀█ ██▒░██   █▌░ ▓██▄   ▒███   ▒▓█    ▄ ▓██ ░▄█ ▒▒███  ▒ ▓██░ ▒░░ ▓██▄   
░▓█▒  ░░██░▓██▒  ▐▌██▒░▓█▄   ▌  ▒   ██▒▒▓█  ▄ ▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓█  ▄░ ▓██▓ ░   ▒   ██▒
░▒█░   ░██░▒██░   ▓██░░▒████▓ ▒██████▒▒░▒████▒▒ ▓███▀ ░░██▓ ▒██▒░▒████▒ ▒██▒ ░ ▒██████▒▒
 ▒ ░   ░▓  ░ ▒░   ▒ ▒  ▒▒▓  ▒ ▒ ▒▓▒ ▒ ░░░ ▒░ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░░░ ▒░ ░ ▒ ░░   ▒ ▒▓▒ ▒ ░
 ░      ▒ ░░ ░░   ░ ▒░ ░ ▒  ▒ ░ ░▒  ░ ░ ░ ░  ░  ░  ▒     ░▒ ░ ▒░ ░ ░  ░   ░    ░ ░▒  ░ ░
 ░ ░    ▒ ░   ░   ░ ░  ░ ░  ░ ░  ░  ░     ░   ░          ░░   ░    ░    ░      ░  ░  ░  
        ░           ░    ░          ░     ░  ░░ ░         ░        ░  ░              ░  
                       ░                      ░                                         


usage: main.py [-h] --url URL

Get sensitive information from javascript files from a give domain

optional arguments:
  -h, --help  show this help message and exit
  --url URL   [+] URL from a domain

{}
{}
""".format(__AUTHOR__,__VERSION__)
    return banner