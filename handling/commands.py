import json
import requests
import handling.utils.messagesend as sender
import handling.utils.creds as cred



def command(message):
    dnd = "https://www.dnd5eapi.co/api/"
    args = list(filter(lambda x: x != "", message["d"]["content"][2:].split(" ")))
    print(args)
    preface = ""
    url = dnd+args[0]+"/"+args[1]
    print("GET: {}".format(url))
    r = requests.get(url)
    if r.status_code == 200:
        sender.send_embed_message(message["d"]["channel_id"], format_data(args[0], r.json()))
    else:
        sender.send_non_embed_message(message["d"]["channel_id"], "Something went wrong, try again and make sure your message is formatted properly. {}".format(r.status_code), False)
        
        
def format_data(cate, jdata):
    if cate == "equipment":
        return equipment_format(jdata)
    elif cate == "classes":
        return class_format(jdata)
    elif cate == "races":
        return race_format(jdata)
    elif cate == "spells":
        return spell_format(jdata)
    elif cate == "monsters":
        return monster_format(jdata)
    elif cate == "conditions":
        return condition_format(jdata)
    elif cate == "damage-types":
        return damage_type_format(jdata)

def equipment_format(jdata):
    message = {
        "content": "",
        "embed": {
            "title": jdata["name"],
            "type": "rich",
            "fields": [
                {
                    "name": "Damage",
                    "value": "{}".format(jdata["damage"]["damage_dice"]+" "+jdata["damage"]["damage_type"]["name"])
                },
                {
                    "name": "Value",
                    "value": "{}".format(str(jdata["cost"]["quantity"])+" "+jdata["cost"]["unit"])
                },
                {
                    "name": "Range",
                    "value": "{}".format(str(jdata["weapon_range"]))
                },
                {
                    "name": "Weight",
                    "value": "{}".format(str(jdata["weight"]))   
                }
            ]
        },
        "tts": False
    }
    return message

def class_format(jdata):
    pass
def race_format(jdata):
    pass
def spell_format(jdata):
    pass
def monster_format(jdata):
    pass
def condition_format(jdata):
    pass
def damage_type_format(jdata):
    pass
