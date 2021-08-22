import json
import requests
import handling.utils.messagesend as sender
import handling.utils.creds as cred
import handling.commands as commandler
import handling.voice as voice

global bot_id
global bot_token
bot_id = cred.bot_id()
bot_token = cred.token()

class Recv_Handler:
    def __init__(self):
        self.v = None
        
    def strip_non_descriptors(self, words, index, im):
        adjs = []    #initialize adjective array
        ret = ""     #return value
        ioffset = 0  #index offset
        with open("handling/adj.txt", "r") as file:     #fill adjs with content from handling/adjs.txt
            for line in file:
                adjs.append(line.strip())
                
        while True:     #look I know while Trues are bad practice but theyre easy
            if(index+ioffset == len(words)-1):              #if the previous word is the last word end prematurely, can't put at the end of while because
                return ret.strip() if len(ret) != 0 else False      #words[index] is always in im[] which would lead to unoptimal iteration times. simply put its a way to catch if the message ends in a adjective(returns adjectives) or in im[](returns False)
            ioffset += 1
            if(words[index+ioffset] == "a" or words[index+ioffset] in im):        #if current word is in im[] or == " a " do not include
                pass
            elif(words[index+ioffset] in adjs):     #if message follows "im (a) <adjective> <etc>" include adjectives
                ret += words[index+ioffset] + " "
            else:                                   #if current word is not " a ", in im[] or an adjective we are done
                ret +=words[index+ioffset]
                return ret.strip()

    def handle(self, message, conn):
        content = message["d"]["content"]  #for simplicity
        
        for i in message["d"]["mentions"]:
            if(int(i["id"]) == bot_id):                                                 #simple ping and response
                sender.send_non_embed_message(message["d"]["channel_id"], "I am here!", False)
        
        for i in message["d"]["mentions"]:
            if(int(i["id"]) == 237948713123708939):                                 #dont fucking ping me
                sender.send_non_embed_message(message["d"]["channel_id"], "Don't bother him", False)
        
        words = content.split(" ")                                                              #dadbot
        im = ["Im", "im", "i'm", "I'm"]
        for i in im:
            if(i in words):
                full_title = self.strip_non_descriptors(words, words.index(i), im)
                if(full_title):
                    sender.send_non_embed_message(message["d"]["channel_id"], "Hi, {}, I'm <@!{}>".format(full_title, bot_id), False)
                    break
        
        if content.startswith("d!"):
            commandler.command(message)
         
        if(content.startswith("!join")):
            self.v = voice.Voice(conn, message["d"]["guild_id"], content.split(" ")[1], bot_id)
            self.v.connect()
            