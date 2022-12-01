#!/usr/bin/env python3
# Version 1.0.0
# Author - Tanishq Rathore

import requests
import configparser
import sys
import os
import pwinput
import argparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    SLANT = '\x1B[3m'


logo = f"""{bcolors.OKCYAN}

  ______     ___ ____     
 /_  __/__  / (_) __/_  __
  / / / _ \\/ / / /_/ / / /
 / / /  __/ / / __/ /_/ / 
/_/  \\___/_/_/_/  \\__, /  
                 /____/   {bcolors.ENDC}{bcolors.SLANT}{bcolors.UNDERLINE}V 1.0.0{bcolors.ENDC}

"""

print(logo)
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', type=str,help=f'📄_Send a file to Telegram channel \t \t {bcolors.BOLD} {bcolors.OKBLUE}-f file.txt{bcolors.ENDC}',default="NO_FILE")
parser.add_argument('-m','--message', type=str,help=f'✉️ _Send a message to Telegram channel \t \t{bcolors.BOLD} {bcolors.OKBLUE} -m "Telify!!!"{bcolors.ENDC}',default="NO_MSG")
args = parser.parse_args()


def sent(CID,API):
    if args.message != 'NO_MSG':
        try:
            apiurl = f'https://api.telegram.org/bot{API}/sendMessage'
            requests.post(apiurl, json={'chat_id': CID, 'text': args.message})
            print(f'[{bcolors.BOLD}{bcolors.OKGREEN}+{bcolors.ENDC}] Message sent')
        except Exception as e:
            print(e)
    elif args.file != 'NO_FILE':
        try:
            files = {'document': open(args.file, 'rb')}
            apiurl = f'https://api.telegram.org/bot{API}/sendDocument?chat_id={CID}'
            requests.post(apiurl, files=files)
            print(f'[{bcolors.BOLD}{bcolors.OKGREEN}+{bcolors.ENDC}] File uploaded')
        except Exception as e:
            print(e)
    elif not sys.stdin.isatty():
        try:
            apiurl = f'https://api.telegram.org/bot{API}/sendMessage'
            requests.post(apiurl, json={'chat_id': CID, 'text': f"{sys.stdin.read()}" })
            print(f'[{bcolors.BOLD}{bcolors.OKGREEN}+{bcolors.ENDC}] stdin data sent')
        except Exception as e:
            print(e)


def main():
    if __name__ == '__main__':
        config = configparser.ConfigParser()
        try: 
            config.read(os.path.join(os.path.expanduser( '~' ),'telify.ini'))
            CHAT_ID = config['TELIFY']['CHATID']
            API_TOKEN = config['TELIFY']['APITOKEN']
            sent(CHAT_ID,API_TOKEN)
        except:
            print(f'[{bcolors.BOLD}{bcolors.OKGREEN}+{bcolors.ENDC}] Please Enter API Token:')
            API_TOKEN = pwinput.pwinput(prompt=f'❯❯ ', mask='*')
            CHAT_ID = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/getUpdates').text.split('"id":')[1].split(',"title":')[0]
            config['TELIFY'] = {'CHATID':CHAT_ID,'APITOKEN':API_TOKEN}
            try:
                with open(os.path.join(os.path.expanduser( '~' ),'telify.ini'),'w') as configfile:
                    config.write(configfile)
                    print(f'[{bcolors.BOLD}{bcolors.OKGREEN}+{bcolors.ENDC}] API Token saved in configuration')
                    apiurl = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
                    requests.post(apiurl, json={'chat_id': CHAT_ID, 'text': 'Telify is now working!!!'})
            except Exception as e:
                print(e)
            exit()


main()