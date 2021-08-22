import json
import requests
import handling.utils.messagesend as sender
import handling.utils.creds as cred
import handling.commands as commandler
import websocket
import threading
import time
import random
import stempeg
import scapy

class Voice:
    def __init__(self, s_gateway, guild_id, channel_id, uid):
        self.gid = guild_id
        self.cid = channel_id
        self.gateway = s_gateway
        self.token = None
        self.endpoint = None
        self.session_id = None
        self.heart = None
        self.v_gateway = None
        self.ms = 0
        self.user_id = uid
        self.ip = None
        self.port = 0
        self.mode = "xsalsa20_poly1305"
        self.enc_key = None
        self.udp_gateway = None
        
    def connect(self):
        voice_state_update = {
            "op": 4,
            "d": {
                "guild_id": self.gid,
                "channel_id": self.cid,
                "self_mute": False,
                "self_deaf": True
            }
        }
        self.gateway.send(json.dumps(voice_state_update))
        v_stat = self.gateway.recv()
        print("VOICE STATE UPDATE-------------------------------------------------")
        print(v_stat)
        v_serv = self.gateway.recv()
        print("VOICE SERVER UPDATE-------------------------------------------------")
        print(v_serv)
        v_serv = json.loads(v_serv)
        v_stat = json.loads(v_stat)
        self.endpoint = "wss://"+v_serv["d"]["endpoint"]
        self.token = v_serv["d"]["token"]
        self.session_id = v_stat["d"]["session_id"]
        self.v_gateway = websocket.create_connection(self.endpoint)
        hb = self.v_gateway.recv()
        print(hb)
        self.ms = json.loads(hb)["d"]["heartbeat_interval"]
        self.heart = threading.Thread(target=self.heartbeat).start()
        voice_identify = {
            "op": 0,
            "d": {
                "server_id": self.gid,
                "user_id": self.user_id,
                "session_id": self.session_id,
                "token": self.token
            }
        }
        print("SEND VREADY-----------------------------------------------")
        self.v_gateway.send(json.dumps(voice_identify))
        v_ready = self.v_gateway.recv()
        print(v_ready)
        v_ready = json.loads(v_ready)
        self.ip = v_ready["d"]["ip"]
        self.port = v_ready["d"]["port"]
        
        
    def heartbeat(self):
        while True:
            hb = {
                "op": 3,
                "d": 1501184119561
            }
            print("VOICE HEARTBEAT-----------------------------------------------")
            print(hb)
            self.v_gateway.send(json.dumps(hb))
            print(self.v_gateway.recv())
            time.sleep(self.ms/1000)