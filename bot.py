import websocket
import json
import requests
import threading 
import time
import handling.MESSAGE_CREATE as msgrecvhandler
import handling.utils.creds as cred

global bot_id
global bot_token
bot_id = cred.bot_id()
bot_token = cred.token()


try:
    cache = None
    with open("cache.json", "r") as jdata:
        cache = json.load(jdata)
    gateway = cache["gateway"]
    global conn 
    conn = websocket.create_connection(gateway+"/?v=8&encoding=json")
except:
    r = requests.get(url="https://www.discord.com/api/v8/gateway").json()
    jdata = {
        "gateway": r["url"]
    }
    print("**[WARNING]** GATEWAY CONNECTION FAILED, OBTAINING NEW URL: " + r["url"])
    with open("cache.json", "w") as outfile:
        json.dump(jdata, outfile)
    conn = websocket.create_connection(r["url"]+"/?v=8&encoding=json")

hb = conn.recv()
global hbrate 
hbrate = json.loads(hb)["d"]["heartbeat_interval"]
print(hb)
    
def resume_session():
    global hbrate
    try:
        cache = None
        with open("cache.json", "r") as jdata:
            cache = json.load(jdata)
        gateway = cache["gateway"]
        conn = websocket.create_connection(gateway+"/?v=8&encoding=json")
    except:
        r = requests.get(url="https://www.discord.com/api/v8/gateway").json()
        jdata = {
            "gateway": r["url"]
        }
        print("**[WARNING]** GATEWAY CONNECTION FAILED, OBTAINING NEW URL: " + r["url"])
        with open("cache.json", "w") as outfile:
            json.dump(jdata, outfile)
        conn = websocket.create_connection(r["url"]+"/?v=8&encoding=json")

    hb = conn.recv()
    hbrate = json.loads(hb)["d"]["heartbeat_interval"]
    print(hb)
    conn.send(json.dumps(json.loads('{"op":1, "d": null}')))
    r = conn.recv()
    print(r)
    
    content = {
        "op": 6, 
        "d": {
            "token": "{}".format(bot_token), 
            "intents": 3584, 
            "properties": {
                "$os": "windows", 
                "$browser": "my_library", 
                "$device": "my_library"
            }
        }, 
        "s": None, 
        "t": None
    }
    conn.send(json.dumps(content))
    r = conn.recv()
    if(r["t"] != "READY"):
        print(r)
        print("**[TERMINATION ERROR]**")
        conn.close()
    
def heartbeat():
    while True:
        try:
            conn.send(json.dumps(json.loads('{"op":1, "d": null}')))
        except:
            print("**[WARN]** HEARTBEAT FAILED, ATTEMPTING HEARTBEAT AGAIN")
            try:
                conn.send(json.dumps(json.loads('{"op":1, "d": null}')))
            except:
                print("**[ERROR]** CONNECTION FAILED, ATTEMPTING RESUME SESSION")
                try:
                    conn.close()
                except:
                    pass
                resume_session()
        time.sleep(hbrate/1000)
        print("**[INFO]** Heartbeat")

hbthread = threading.Thread(target=heartbeat)
hbthread.start()

r = conn.recv()
print(r)

content = {
    "op": 2, 
    "d": {
        "token": "{}".format(bot_token), 
        "intents": 641, 
        "properties": {
            "$os": "windows", 
            "$browser": "my_library", 
            "$device": "my_library"
        }
    }, 
    "s": None, 
    "t": None
}

conn.send(json.dumps(content))
r = conn.recv()
print(r)
print("**[INFO]** SYSTEM READY")
msghandler = msgrecvhandler.Recv_Handler()
while conn:
    r = conn.recv()
    print("RECV: ---------------------------------------------------------------\n{}".format(r))
    r = json.loads(r)
    if((r["t"] == "MESSAGE_CREATE") and r["d"]["author"]["id"] != str(bot_id)):
        response = msghandler.handle(r, conn)
conn.close()