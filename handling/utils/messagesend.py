import json
import requests
import handling.utils.creds as cred

global bot_id
global bot_token
bot_id = cred.bot_id()
bot_token = cred.token()

def send_non_embed_message(channel_id, message, tts):
    url = "https://discord.com/api/v8/channels/{}/messages".format(channel_id)
    headers = {
        "Authorization": "Bot {}".format(bot_token)
    }
    
    payload = {
        "content": message,
        "tts": tts
    }
    
    r = requests.post(url=url, headers=headers, json=payload)
    print("SEND: ---------------------------------------------------------------\nPOST {}: {}".format(url, payload))
    
def send_embed_message(channel_id, payload):
    url = "https://discord.com/api/v8/channels/{}/messages".format(channel_id)
    headers = {
        "Authorization": "Bot {}".format(bot_token)
    }
    
    r = requests.post(url=url, headers=headers, json=payload)
    print("SEND: ---------------------------------------------------------------\nPOST {}: {}".format(url, payload))