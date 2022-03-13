import requests
import json
import random
import string
from time import sleep
from datetime import datetime as dt
from termcolor import colored

def id_generator(size=8, characters=string.ascii_uppercase + string.digits):
    rand = ''.join(random.choice(characters) for _ in range(size))
    return rand

def send_message(webhook_url):
    username = id_generator()
    message = "@everyone"
    data = json.dumps({
        "content": message,
        "username": username,
        "tts": False
    })

    header = {
        "content-type": "application/json"
    }

    response = requests.post(webhook_url, data, headers=header)

    now = dt.now()
    s = now.strftime("%H:%M:%S")

    if not response.ok:
        if response.status_code == 429:
            print(colored('[' + s + ']>', 'white'), colored("[-] Couldn't send webhook!", 'red'))
        else:
            print(colored('[' + s + ']>', 'white'), colored("[-] Couldn't send webhook!", 'red'))
            print(response.reason)
            print(response.text)
        return False
    else:
        print(colored('[' + s + ']>', 'white'), colored('[+] Successfully sent webhook!', 'green'))
        return True

webhook = input("Webhook URL: ")
attempt_count = 0
sent_count = 0

print("Started spamming the webhook! CTRL + C to stop")
sleep(0.5)

failed_previous = False

try:
    while True:
        if (send_message(webhook)):
            sent_count += 1
            failed_previous = False
        else:
            if failed_previous:
                print("Waiting 30 seconds! - didn't work second time!")
                sleep(29)
            else:
                sleep(0.6)
            failed_previous = True
        attempt_count += 1
except KeyboardInterrupt:
    print("keyboardInterrupt caught! Sent {} messages.".format(sent_count))
    pass
