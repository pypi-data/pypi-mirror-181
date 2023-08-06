import datetime
import libraryArsein.encoder
from libraryArsein.encoder import encoderjson
from libraryArsein.encoder import encoder_photo
import libraryArsein.copyright
from libraryArsein.copyright import copyright_Arsein
from libraryArsein.Device import DeviceTelephone
import json
from json import dumps, loads
import random
from random import randint, choice
import libraryArsein.clines_ph_web
from libraryArsein.clines_ph_web import clien
from requests import post, get
import urllib
from urllib import request
from pathlib import Path
import libraryArsein.send_server
from libraryArsein.send_server import send_server_rubika
from re import findall
from tinytag import TinyTag
import libraryArsein.PostData
from libraryArsein.PostData import http,httpfiles
import asyncio
from asyncio import run


class Robot_Rubika:
    ser_full = send_server_rubika()
    s = ser_full.server_full()
    ser_file = send_server_rubika()
    b = ser_file.server_files()
    def __init__(self, Sh_account: str):
        self.Auth = str("".join(findall(r"\w",Sh_account)))
        self.prinet = copyright_Arsein.arsein
        self.enc = encoderjson(Sh_account)
        if self.Auth.__len__() < 32:
            print("شناسه اکانت خود را درست وارد نمائید")
            print(" ")
            print("........")
            print("هم اکنون شناسه اکانت خود را در سورس مورد نظر وارد نمائید و از اول ران کنید")
        else:
            if self.Auth.__len__() > 32:
                print("شناسه اکانت خود را درست وارد نمائید")
                print(" ")
                print("........")
                print("هم اکنون شناسه اکانت خود را در سورس مورد نظر وارد نمائید و از اول ران کنید")

    def sendMessage(self, chat_id,text,metadata=[],message_id=None):
        inData = {
            "method":"sendMessage",
            "input":{
                "object_guid":chat_id,
                "rnd":f"{randint(100000,999999999)}",
                "text":text,
                "reply_to_message_id":message_id
            },
            "client": clien.web
        }
        if metadata != [] : inData["input"]["metadata"] = {"meta_data_parts":metadata}

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def editMessage(self, gap_guid, newText, message_id):
        inData = {
            "method":"editMessage",
            "input":{
                "message_id":message_id,
                "object_guid":gap_guid,
                "text":newText
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def deleteMessages(self, chat_id, message_ids):
        inData = {
            "method":"deleteMessages",
            "input":{
                "object_guid":chat_id,
                "message_ids":message_ids,
                "type":"Global"
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def getMessagefilter(self, chat_id, filter_whith):
        inData = {
            "method":"getMessages",
            "input":{
                "filter_type":filter_whith,
                "max_id":"NaN",
                "object_guid":chat_id,
                "sort":"FromMax"
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get("data").get("messages")
                break
            except: continue

    def getMessages(self, chat_id, min_id):
        inData = {
            "method":"getMessagesInterval",
            "input":{
                "object_guid":chat_id,
                "middle_message_id":min_id
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get("data").get("messages")
                break
                break
            except: continue

    def getChats(self, start_id=None):
        inData = {
            "method":"getChats",
            "input":{
                "start_id":start_id
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get("data").get("chats")
                break
            except: continue

    def deleteUserChat(self, user_guid, last_message):
        inData = {
            "method":"deleteUserChat",
            "input":{
                "last_deleted_message_id":last_message,
                "user_guid":user_guid
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def getInfoByUsername(self, username):
        inData = {
            "method":"getObjectByUsername",
            "input":{
                "username":username
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def banGroupMember(self, chat_id, user_id):
        inData = {
            "method":"banGroupMember",
            "input":{
                "group_guid": chat_id,
                "member_guid": user_id,
                "action":"Set"
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def unbanGroupMember(self, chat_id, user_id):
        inData = {
            "method":"banGroupMember",
            "input":{
                "group_guid": chat_id,
                "member_guid": user_id,
                "action":"Unset"
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def getGroupInfo(self, chat_id):
        inData = {
            "method":"getGroupInfo",
            "input":{
                "group_guid": chat_id
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def invite(self, chat_id, user_ids):
        inData = {
            "method":"addGroupMembers",
            "input":{
                "group_guid": chat_id,
                "member_guids": user_ids
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def inviteChannel(self, chat_id, user_ids):
        inData = {
            "method":"addChannelMembers",
            "input":{
                "channel_guid": chat_id,
                "member_guids": user_ids
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def getGroupAdmins(self, chat_id):
        inData = {
            "method":"getGroupAdminMembers",
            "input":{
                "group_guid":chat_id
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def getChannelInfo(self, channel_guid):
        inData = {
            "method":"getChannelInfo",
            "input":{
                "channel_guid":channel_guid
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def AddNumberPhone(self, first_num, last_num, numberPhone):
        inData = {
            "method":"addAddressBook",
            "input":{
                "first_name":first_num,
                "last_name":last_num,
                "phone":numberPhone
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue



    def getMessagesInfo(self, chat_id, message_ids):
        inData = {
            "method":"getMessagesByID",
            "input":{
                "object_guid": chat_id,
                "message_ids": message_ids
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get("data").get("messages")
                break
            except: continue

    def getMessages_info_android(self, chat_id, message_ids):
        inData = {
            "method":"getMessagesByID",
            "input":{
                "message_ids": message_ids,
                "object_guid": chat_id
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get("data").get("messages")
                break
            except: continue


    def setMembersAccess(self, chat_id, access_list):
        inData = {
            "method":"setGroupDefaultAccess",
            "input":{
                "access_list": access_list,
                "group_guid": chat_id
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData)))
                break
            except: continue

    def getGroupMembers(self, chat_id, start_id=None):
        inData = {
            "method":"getGroupAllMembers",
            "input":{
                "group_guid": chat_id,
                "start_id": start_id
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def getGroupLink(self, chat_id):
        inData = {
            "method":"getGroupLink",
            "input":{
                "group_guid":chat_id
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get("data").get("join_link")
                break
            except: continue

    def getChannelLink(self, chat_id):
        inData = {
            "method":"getChannelLink",
            "input":{
                "group_guid":chat_id
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get("data").get("join_link")
                break
            except: continue

    def changeGroupLink(self, chat_id):
        inData = {
            "method":"setGroupLink",
            "input":{
                "group_guid": chat_id
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get("data").get("join_link")
                break
            except: continue

    def changeChannelLink(self, chat_id):
        inData = {
            "method":"setChannelLink",
            "input":{
                "channel_guid": chat_id
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get("data").get("join_link")
                break
            except: continue

    def setGroupTimer(self, chat_id, time):
        inData = {
            "method":"editGroupInfo",
            "input":{
                "group_guid": chat_id,
                "slow_mode": time,
                "updated_parameters":["slow_mode"]
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def setGroupAdmin(self, chat_id, user_id):
        inData = {
            "method":"setGroupAdmin",
            "input":{
                "group_guid": chat_id,
                "access_list":["PinMessages","DeleteGlobalAllMessages","BanMember","SetMemberAccess"],
                "action": "SetAdmin",
                "member_guid": user_id
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def deleteGroupAdmin(self,c,user_id):
        inData = {
            "method":"setGroupAdmin",
            "input":{
                "group_guid": c,
                "action": "UnsetAdmin",
                "member_guid": user_id
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def setChannelAdmin(self, chat_id, user_id, access_list=[]):
        inData = {
            "method":"setGroupAdmin",
            "input":{
                "group_guid": chat_id,
                "access_list": access_list,
                "action": "SetAdmin",
                "member_guid": user_id
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def getStickersByEmoji(self,emojee):
        inData = {
            "method":"getStickersByEmoji",
            "input":{
                "emoji_character": emojee,
                "suggest_by": "All"
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get("data").get("stickers")
                break
            except: continue


    def setActionChatun(self,guid):
        inData = {
            "method":"setActionChat",
            "input":{
                "action": "Unmute",
                "object_guid": guid
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def setActionChatmut(self,guid):
        inData = {
            "method":"setActionChat",
            "input":{
                "action": "Mute",
                "object_guid": guid
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def sendPoll(self,guid,SOAL,LIST):
        inData = {
            "method":"createPoll",
            "input":{
                "allows_multiple_answers": "false",
                "is_anonymous": "true",
                "object_guid": guid,
                "options":LIST,
                "question":SOAL,
                "rnd":f"{randint(100000,999999999)}",
                "type":"Regular"
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def forwardMessages(self, From, message_ids, to):
        inData = {
            "method":"forwardMessages",
            "input":{
                "from_object_guid": From,
                "message_ids": message_ids,
                "rnd": f"{randint(100000,999999999)}",
                "to_object_guid": to
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def chatGroupvisit(self,guid,visiblemsg):
        inData = {
            "method":"editGroupInfo",
            "input":{
                "chat_history_for_new_members": "Visible",
                "group_guid": guid,
                "updated_parameters": visiblemsg
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def chatGrouphidden(self,guid,hiddenmsg):
        inData = {
            "method":"editGroupInfo",
            "input":{
                "chat_history_for_new_members": "Hidden",
                "group_guid": guid,
                "updated_parameters": hiddenmsg
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def pin(self, chat_id, message_id):
        inData = {
            "method":"setPinMessage",
            "input":{
                "action":"Pin",
                "message_id": message_id,
                "object_guid": chat_id
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def unpin(self, chat_id, message_id):
        inData = {
            "method":"setPinMessage",
            "input":{
                "action":"Unpin",
                "message_id": message_id,
                "object_guid": chat_id
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def logout(self):
        inData = {
            "method":"logout",
            "input":{},
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def joinGroup(self, link):
        hashLink = link.split("/")[-1]
        inData = {
            "method":"joinGroup",
            "input":{
                "hash_link": hashLink
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def joinChannel(self, link):
        hashLink = link.split("/")[-1]
        inData = {
            "method":"joinChannelByLink",
            "input":{
                "hash_link": hashLink
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def deleteChatHistory(self, chat_id, msg_id):
        inData = {
            "method":"deleteChatHistory",
            "input":{
                "last_message_id": msg_id,
                "object_guid": chat_id
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def leaveGroup(self,chat_id):
        if "https://" in chat_id:
            guid = Robot_Rubika.joinGroup(self,chat_id)["data"]["group"]["group_guid"]
        else:
            guid = chat_id

        inData = {
            "method":"leaveGroup",
            "input":{
                "group_guid": guid
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def editnameGroup(self,groupgu,namegp,biogp=None):
        inData = {
            "method":"editGroupInfo",
            "input":{
                "description": biogp,
                "group_guid": groupgu,
                "title":namegp,
                "updated_parameters":["title","description"]
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def editbioGroup(self,groupgu,biogp,namegp=None):
        inData = {
            "method":"editGroupInfo",
            "input":{
                "description": biogp,
                "group_guid": groupgu,
                "title":namegp,
                "updated_parameters":["title","description"]
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def joinChannelByID(self, chat_id:str):
        IDE = chat_id.split("@")[-1]
        GUID = Robot_Rubika.getInfoByUsername(self,IDE)["data"]["channel"]["channel_guid"]
        inData = {
            "method":"joinChannelAction",
            "input":{
                "action": "Join",
                "channel_guid": GUID
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def LeaveChannel(self,chat_id):
        if "https://" in chat_id:
            guid = Robot_Rubika.joinChannel(self,chat_id)["data"]["group"]["group_guid"]
        else:
            guid = chat_id

        inData = {
            "method":"joinChannelAction",
            "input":{
                "action": "Leave",
                "channel_guid": chat_id
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def block(self, chat_id):
        inData = {
            "method":"setBlockUser",
            "input":{
                "action": "Block",
                "user_guid": chat_id
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def unblock(self, chat_id):
        inData = {
            "method":"setBlockUser",
            "input":{
                "action": "Unblock",
                "user_guid": chat_id
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def getChannelMembers(self, channel_guid, text=None, start_id=None):
        inData = {
            "method":"getChannelAllMembers",
            "input":{
                "channel_guid":channel_guid,
                "search_text":text,
                "start_id":start_id,
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def startVoiceChat(self, chat_id):
        inData = {
            "method":"createGroupVoiceChat",
            "input":{
                "chat_guid":chat_id
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def editVoiceChat(self,chat_id,voice_chat_id, title):
        inData = {
            "method":"setGroupVoiceChatSetting",
            "input":{
                "chat_guid":chat_id,
                "voice_chat_id" : voice_chat_id,
                "title" : title ,
                "updated_parameters": ["title"]
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def getUserInfo(self, chat_id):
        inData = {
            "method":"getUserInfo",
            "input":{
                "user_guid":chat_id
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def finishVoiceChat(self, chat_id, voice_chat_id):
        inData = {
            "method":"discardGroupVoiceChat",
            "input":{
                "chat_guid":chat_id,
                "voice_chat_id" : voice_chat_id
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def getChatsUpdate(self):
        time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
        inData = {
            "method":"getChatsUpdates",
            "input":{
                "state":time_stamp,
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get('data').get('chats')
                break
            except: continue

    def getMessagesChats(self, start_id=None):
        time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
        inData = {
            "method":"getChats",
            "input":{
                "start_id":start_id
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get('data').get('chats')
                break
            except: continue

    def SeeGroupBylink(self,link_gh):
        inData = {
            "method":"groupPreviewByJoinLink",
            "input":{
                "hash_link": link_gh
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get("data")
                break
            except: continue

    def _requestSendFile(self, file):
        inData = {
            "method":"requestSendFile",
            "input":{
                "file_name": str(file.split("/")[-1]),
                "mime": file.split(".")[-1],
                "size": Path(file).stat().st_size
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.b,self.Auth,inData))).get("data_enc"))).get("data")
                break
            except: continue

    def _uploadFile(self, file):
        if not "http" in file:
            REQUES = Robot_Rubika._requestSendFile(self, file)
            bytef = open(file,"rb").read()

            hash_send = REQUES["access_hash_send"]
            file_id = REQUES["id"]
            url = REQUES["upload_url"]

            header = {
                'auth':self.Auth,
                'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
                'chunk-size':str(Path(file).stat().st_size),
                'file-id':str(file_id),
                'access-hash-send':hash_send,
                "content-type": "application/octet-stream",
                "content-length": str(Path(file).stat().st_size),
                "accept-encoding": "gzip",
                "user-agent": "okhttp/3.12.1"
            }

            if len(bytef) <= 131072:
                header["part-number"], header["total-part"] = "1","1"

                while True:
                    try:
                        loop = asyncio.get_event_loop()
                        j = loop.run_until_complete(httpfiles(url,bytef,header))
                        j = loads(j)['data']['access_hash_rec']
                        break
                    except Exception as e:
                        continue

                return [REQUES, j]
            else:
                t = round(len(bytef) / 131072 + 1)
                for i in range(1,t+1):
                    if i != t:
                        k = i - 1
                        k = k * 131072
                        while True:
                            try:
                                header["chunk-size"], header["part-number"], header["total-part"] = "131072", str(i),str(t)
                                loop = asyncio.get_event_loop()
                                o = loop.run_until_complete(httpfiles(url,bytef[k:k + 131072],header))
                                o = loads(o)['data']
                                break
                            except Exception as e:
                                continue
                    else:
                        k = i - 1
                        k = k * 131072
                        while True:
                            try:
                                header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:])), str(i),str(t)
                                loop = asyncio.get_event_loop()
                                p = loop.run_until_complete(httpfiles(url,bytef[k:],header))
                                p = loads(p)['data']['access_hash_rec']
                                break
                            except Exception as e:
                                continue
                        return [REQUES, p]
        else:
            REQUES = {
                "method":"requestSendFile",
                "input":{
                    "file_name": file.split("/")[-1],
                    "mime": file.split(".")[-1],
                    "size": len(get(file).content)
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.b,self.Auth,inData))).get("data_enc"))).get("data")
                break
            except: continue

            hash_send = REQUES["access_hash_send"]
            file_id = REQUES["id"]
            url = REQUES["upload_url"]
            bytef = get(file).content

            header = {
                'auth':self.Auth,
                'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
                'chunk-size':str(len(get(file).content)),
                'file-id':str(file_id),
                'access-hash-send':hash_send,
                "content-type": "application/octet-stream",
                "content-length": str(len(get(file).content)),
                "accept-encoding": "gzip",
                "user-agent": "okhttp/3.12.1"
            }

            if len(bytef) <= 131072:
                header["part-number"], header["total-part"] = "1","1"

                while True:
                    try:
                        loop = asyncio.get_event_loop()
                        j = loop.run_until_complete(httpfiles(url,bytef,header))
                        j = loads(j)['data']['access_hash_rec']
                        break
                    except Exception as e:
                        continue

                return [REQUES, j]
            else:
                t = round(len(bytef) / 131072 + 1)
                for i in range(1,t+1):
                    if i != t:
                        k = i - 1
                        k = k * 131072
                        while True:
                            try:
                                header["chunk-size"], header["part-number"], header["total-part"] = "131072", str(i),str(t)
                                loop = asyncio.get_event_loop()
                                o = loop.run_until_complete(httpfiles(url,bytef[k:k + 131072],header))
                                o = loads(o)['data']
                                break
                            except Exception as e:
                                continue
                    else:
                        k = i - 1
                        k = k * 131072
                        while True:
                            try:
                                header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:])), str(i),str(t)
                                loop = asyncio.get_event_loop()
                                p = loop.run_until_complete(httpfiles(url,bytef[k:],header))
                                p = loads(p)['data']['access_hash_rec']
                                break
                            except Exception as e:
                                continue
                        return [REQUES, p]




    @staticmethod
    def _getImageSize(image_bytes:bytes):
        import io, PIL.Image
        im = PIL.Image.open(io.BytesIO(image_bytes))
        width, height = im.size
        return [width , height]



    def uploadAvatar_replay(self,myguid,files_ide):
        inData = {
            "method":"uploadAvatar",
            "input":{
                "object_guid":myguid,
                "thumbnail_file_id":files_ide,
                "main_file_id":files_ide
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def uploadAvatar(self,myguid,main,thumbnail=None):
        mainID = str(Robot_Rubika._uploadFile(self, main)[0]["id"])
        thumbnailID = str(Robot_Rubika._uploadFile(self, thumbnail or main)[0]["id"])
        inData = {
            "method":"uploadAvatar",
            "input":{
                "object_guid":myguid,
                "thumbnail_file_id":thumbnailID,
                "main_file_id":mainID
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def Devices_rubika(self):
        inData = {
            "method":"getMySessions",
            "input":{

            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def addFolder(self, Name = "Arsein", include_chat = None,include_object = None ,exclude_chat = None,exclude_object = None):
        inData = {
            "method":"addFolder",
            "input":{
                "exclude_chat_types": exclude_chat,
                "exclude_object_guids": exclude_object,
                "include_chat_types": include_chat,
                "include_object_guids": include_object,
                "is_add_to_top":True,
                "name": Name
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def deleteFolder(self,folder_id):
        inData = {
            "method":"deleteFolder",
            "input":{
                "folder_id": folder_id
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def addChannel(self,title,typeChannell,bio,guidsUser = None):
        inData = {
            "method":"addChannel",
            "input":{
                "addChannel": typeChannell,
                "description": bio,
                "member_guids": guidsUser,
                "title": title,
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def addGroup(self,title,guidsUser = None):
        inData = {
            "method":"addGroup",
            "input":{
                "member_guids": guidsUser,
                "title": title
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def breturn(self,start_id = None):
        inData = {
            "method":"getBreturnUsers",
            "input":{
                "start_id": start_id
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get("data").get("abs_users")
                break
            except: continue

    def CountOnline(self,guid):
        inData = {
            "method":"getGroupOnlineCount",
            "input":{
                "group_guid": guid
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get('data').get('online_count')

                break
            except: continue

    def editUser(self,first_name = None,last_name = None,bio = None):
        inData = {
            "method":"updateProfile",
            "input":{
                "bio": bio,
                "first_name": first_name,
                "last_name": last_name,
                "updated_parameters":["first_name","last_name","bio"]
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def editusername(self,username):
        inData = {
            "method":"updateUsername",
            "input":{
                "username": username
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def ProfileEdit(self,first_name = None,last_name = None,bio = None,username = None):
        while 1:
            try:
                Robot_Rubika.editUser(self,first_name = first_name,last_name = last_name,bio = bio)
                Robot_Rubika.editusername(self,username)
                ok = "ok"
                break
                return ok
            except:continue


    def getChatGroup(self,guid_gap):
        while 1:
            try:
                lastmessages = Robot_Rubika.getGroupInfo(self, guid_gap)["data"]["chat"]["last_message_id"]
                messages = Robot_Rubika.getMessages(self, guid_gap, lastmessages)
                return messages
                break
            except:
                continue


    def getChatChannel(self,guid_ch):
        while 1:
            try:
                lastmessages = Robot_Rubika.getChannelInfo(self, guid_ch)["data"]["chat"]["last_message_id"]
                messages = Robot_Rubika.getMessages(self, guid_ch, lastmessages)
                return messages
                break
            except:
                continue


    def tmp_rubik():
        tmp_session = ""
        choices = [*"abcdefghijklmnopqrstuvwxyz0123456789"]
        for i in range(32): tmp_session += choice(choices)
        return tmp_session



    def SendCodeSMS(self,phonenumber):
        tmp = Robot_Rubika.tmp_rubik()
        enc = encoderjson(tmp)
        inData = {
            "method":"sendCode",
            "input":{
                "phone_number":f"98{phonenumber[1:]}",
                "send_type":"SMS"
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def GetCodeSMS(self,phonenumber):
        tmp = Robot_Rubika.tmp_rubik()
        enc = encoderjson(tmp)
        inData = {
            "method":"sendCode",
            "input":{
                "phone_number":f"98{phonenumber[1:]}",
                "send_type":"Internal"
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def Send_Code_pass(self,phone_number:str,pass_you=None):
        tmp = Robot_Rubika.tmp_rubik()
        enc = encoderjson(tmp)
        inData = {
            "method":"sendCode",
            "input":{
                "pass_key":pass_you,
                "phone_number": f"98{phone_number[1:]}",
                "send_type":'SMS'
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def signIn(phone_number,phone_code_hash,phone_code):
        tmp = Robot_Rubika.tmp_rubik()
        enc = encoderjson(tmp)
        inData = {
            "method":"signIn",
            "input":{
                "phone_number":f"98{phone_number[1:]}",
                "phone_code_hash":phone_code_hash,
                "phone_code":phone_code
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def registerDevice(auth, device=DeviceTelephone.defaultDevice):
        enc = encoderjson(auth)
        while 1:
            try:
                loop = asyncio.get_event_loop()
                ersal = loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                return ersal
                break
            except:
                continue

    def AUTH(readfile):
        while 1:
            try:
                with open(f"{readfile}", "r") as file:
                    jget = json.load(file)
                    s = jget["data"]["auth"]
                    regs = Robot_Rubika.registerDevice(s)
                    return regs
            except:continue


    def getServiceInfo(self, guid):
        inData = {
            "method":"getServiceInfo",
            "input":{
                "service_guid": guid
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def ClearAccounts(self):
        inData = {
            "method":"terminateOtherSessions",
            "input":{},
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def HidePhone(self,**kwargs):
        inData = {
            "method":"setSetting",
            "input": {
                "settings": kwargs,
                "update_parameters":["show_my_phone_number"]
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def HideOnline(self,**kwargs):
        inData = {
            "method":"setSetting",
            "input": {
                "settings": kwargs,
                "update_parameters":["show_my_last_online"]
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def Postion(self,ChG,guiduser):
        inData = {
            "method":"requestChangeObjectOwner",
            "input": {
                "object_guid": ChG,
                "new_owner_user_guid": guiduser
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def getPostion(self,guid):
        inData = {
            "method":"getPendingObjectOwner",
            "input": {
                "object_guid": guid
            },
            "client": clien.android
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def twolocks(self,ramz,hide):
        inData = {
            "method":"setupTwoStepVerification",
            "input": {
                "hint": hide,
                "password": ramz
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                locked = loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                if locked["status"] == 'ERROR_GENERIC':
                    return locked["client_show_message"]["link"]["alert_data"]["message"]
                    break
                else:
                    return locked
                    break
            except: continue

            # سرچ در در اکانت کاربر
    def search_inaccount(self,text):
        inData = {
            "method":"searchGlobalMessages",
            "input": {
                "search_text": text,
                "start_id": 0,
                "type": "Text"
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                getsearchm =  loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get("data").get("messages")
                for s in getsearchm:
                    return s
                    break
            except: continue

# سرچ در کل روبیکا
    def search_inrubika(self,text):
        inData = {
            "method":"searchGlobalObjects",
            "input": {
                "search_text": text
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc"))).get("data").get('objects')
                break
            except: continue

    def sendsticker(self,guid,emoji,w_h_rati,sticker_id,file_id,access_hash,set_id):
        inData = {
            "method": "sendMessage",
            "input": {
                "object_guid": guid,
                "rnd": f"{randint(100000,999999999)}",
                "sticker": {
                  "emoji_character": emoji,
                  "w_h_ratio": w_h_rati,
                  "sticker_id": sticker_id,
                  "file": {
                    "file_id": file_id,
                    "mime": "png",
                    "dc_id": 32,
                    "access_hash_rec": access_hash,
                    "file_name": "sticker.png"
                  },
                  "sticker_set_id": set_id
                }
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def votePoll(self,votePoll):
        inData = {
            "method":"votePoll",
            "input": {
                "poll_id": votePoll,
                "selection_index": 0
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def getAbsObjects(self,guids):
        inData = {
            "method":"getAbsObjects",
            "input": {
                "objects_guids": guids
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def info_LinkPost(self,linkpost):
        inData = {
            "method":"getLinkFromAppUrl",
            "input": {
                "app_url": linkpost
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def getContactsLastOnline(self,user_guids:list):
        inData = {
            "method":"getContactsLastOnline",
            "input": {
                "user_guids": user_guids
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def getChatAds(self):
        time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
        inData = {
            "method":"getChatAds",
            "input": {
                "state": time_stamp
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def Sign_messageChannel(self,guidchannel,sing):
        inData = {
            "method":"editChannelInfo",
            "input": {
                "channel_guid": guidchannel,
                "sign_messages": sing,
                "updated_parameters": ["sign_messages"]
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def Join_to_ChG(self,canjoin):
        if canjoin == "مخاطبین":
            inData = {"method":"setSetting","input":{"settings":{"can_join_chat_by":"MyContacts"},"update_parameters":["can_join_chat_by"]},"client":clien.web}
        elif canjoin == "همه":
            inData = {"method":"setSetting","input":{"settings":{"can_join_chat_by":"Everybody"},"update_parameters":["can_join_chat_by"]},"client":clien.web}

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def set_typechannel(self,guidchannel,typeChannell):
        if typeChannell == "خصوصی":
            inData = {"method":"editChannelInfo","input":{"channel_guid":guidchannel,"channel_type":"Private","updated_parameters":["channel_type"]},"client":clien.web}
        elif typeChannell == "عمومی":
            inData = {"method":"editChannelInfo","input":{"channel_guid":guidchannel,"channel_type":"Public","updated_parameters":["channel_type"]},"client":clien.web}

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def changeChannel_ID(self,guidchannel,username):
        inData = {
            "method":"updateChannelUsername",
            "input": {
                "channel_guid": guidchannel,
                "username": username
            },
            "client": clien.web
        }

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.s,self.Auth,inData))).get("data_enc")))
                break
            except: continue

                


    def sendDocument(self, chat_id, file, caption=None, message_id=None):
        uresponse = Robot_Rubika._uploadFile(self, file)
        file_id = str(uresponse[0]["id"])
        mime = file.split(".")[-1]
        dc_id = uresponse[0]["dc_id"]
        access_hash_rec = uresponse[1]
        file_name = file.split("/")[-1]
        size = str(len(get(file).content if "http" in file else open(file,"rb").read()))

        inData = {
            "method":"sendMessage",
            "input":{
                "object_guid":chat_id,
                "reply_to_message_id":message_id,
                "rnd":f"{randint(100000,999999999)}",
                "file_inline":{
                    "dc_id":str(dc_id),
                    "file_id":str(file_id),
                    "type":"File",
                    "file_name":file_name,
                    "size":size,
                    "mime":mime,
                    "access_hash_rec":access_hash_rec
                }
            },
            "client": clien.web
        }

        if caption != None: inData["input"]["text"] = caption


        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.b,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def sendDocument_rplay(self,chat_id,file_id,mime,dc_id,access_hash_rec,file_name,size,caption=None,message_id=None):
        inData = {
            "method":"sendMessage",
            "input":{
                "object_guid":chat_id,
                "reply_to_message_id":message_id,
                "rnd":f"{randint(100000,999999999)}",
                "file_inline":{
                    "dc_id":str(dc_id),
                    "file_id":str(file_id),
                    "type":"File",
                    "file_name":file_name,
                    "size":size,
                    "mime":mime,
                    "access_hash_rec":access_hash_rec
                }
            },
            "client": clien.web
        }

        if caption != None: inData["input"]["text"] = caption


        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.b,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def sendVoice(self, chat_id, file, time, caption=None, message_id=None):
        uresponse = Robot_Rubika._uploadFile(self, file)
        file_id = str(uresponse[0]["id"])
        mime = file.split(".")[-1]
        dc_id = uresponse[0]["dc_id"]
        access_hash_rec = uresponse[1]
        file_name = file.split("/")[-1]
        size = str(len(get(file).content if "http" in file else open(file,"rb").read()))

        inData = {
                "method":"sendMessage",
                "input":{
                    "file_inline": {
                        "dc_id": dc_id,
                        "file_id": file_id,
                        "type":"Voice",
                        "file_name": file_name,
                        "size": size,
                        "time": time,
                        "mime": mime,
                        "access_hash_rec": access_hash_rec,
                    },
                    "object_guid":chat_id,
                    "rnd":f"{randint(100000,999999999)}",
                    "reply_to_message_id":message_id
                },
                "client": clien.web
            }

        if caption != None: inData["input"]["text"] = caption


        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.b,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def sendGif(self, chat_id, file, caption=None, message_id=None, thumbnail=None):
        uresponse = Robot_Rubika._uploadFile(self, file)
        if thumbnail == None: thumbnail = r"/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDACAWGBwYFCAcGhwkIiAmMFA0MCwsMGJGSjpQdGZ6eHJm\ncG6AkLicgIiuim5woNqirr7EztDOfJri8uDI8LjKzsb/2wBDASIkJDAqMF40NF7GhHCExsbGxsbG\nxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsb/wAARCAAyADIDASIA\nAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQA\nAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3\nODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWm\np6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEA\nAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSEx\nBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElK\nU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3\nuLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDXqCXo\nasVXk70DKwHNSBaRRzUgrnZqMUfMKtkcCq24KcmntdxgDmtIEyJ8UVB9ti9aKskmB4qJ/uk1L2qC\nZtsZpiII5P3hB6VDLOySZ7UyVJDEWWoXLGD5uoqFHQtvUnln3rkVB5bv3qqk3Y1filUKM09kCV2R\nfZ39aKtectFK7K5URwagzrila4klcJiqdtbsrA5q+jLE4ZhVXsyErq5bCFYAMVQuVYKVC9av/akc\ncGmy4ZeKaIaZgeWVlANX1jDKKbdRYYNQJQqdamRpAk8pfWiq/n+9FSWPtifM61LcdKKKctyIbEMJ\nO4c1oj7lFFUiWQXH+qNZLmiihjiNzRRRUlH/2Q==\n"
        file_id = str(uresponse[0]["id"])
        mime = file.split(".")[-1]
        dc_id = uresponse[0]["dc_id"]
        access_hash_rec = uresponse[1]
        file_name = file.split("/")[-1]
        size = str(len(get(file).content if "http" in file else open(file,"rb").read()))
        time =  round(TinyTag.get(file).duration * 1000)

        inData = {
                "method":"sendMessage",
                "input":{
                    "file_inline": {
                        "access_hash_rec":access_hash_rec,
                        "auto_play":False,
                        "dc_id":dc_id,
                        "file_id":file_id,
                        "file_name":file_name,
                        "height":360,
                        "mime":mime,
                        "size":size,
                        "thumb_inline":thumbnail,
                        "time":time,
                        "type":"Gif",
                        "width":360,
                    },
                    "is_mute":False,
                    "object_guid":chat_id,
                    "rnd":f"{randint(100000,999999999)}",
                    "reply_to_message_id":message_id
                },
                "client": clien.android
            }

        if caption != None: inData["input"]["text"] = caption


        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.b,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def sendVideo(self, chat_id, file, caption=None, message_id=None):
        uresponse = Robot_Rubika._uploadFile(self, file)
        file_id = str(uresponse[0]["id"])
        mime = file.split(".")[-1]
        dc_id = uresponse[0]["dc_id"]
        access_hash_rec = uresponse[1]
        file_name = file.split("/")[-1]
        size = str(len(get(file).content if "http" in file else open(file,"rb").read()))
        time =  round(TinyTag.get(file).duration * 1000)

        inData = {
                "method":"sendMessage",
                "input":{
                    "file_inline": {
                        "access_hash_rec":access_hash_rec,
                        "auto_play":False,
                        "dc_id":dc_id,
                        "file_id":file_id,
                        "file_name":file_name,
                        "height":360,
                        "mime":mime,
                        "size":size,
                        "thumb_inline":file,
                        "time":time,
                        "type":"Video",
                        "width":360,
                    },
                    "is_mute":False,
                    "object_guid":chat_id,
                    "rnd":f"{randint(100000,999999999)}",
                    "reply_to_message_id":message_id
                },
                "client": clien.android
            }

        if caption != None: inData["input"]["text"] = caption


        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.b,self.Auth,inData))).get("data_enc")))
                break
            except: continue


    def sendPhoto(self, chat_id, file, size=[], thumbnail=None, caption=None, message_id=None):
        uresponse = Robot_Rubika._uploadFile(self, file)
        if thumbnail == None: thumbnail = 'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAIAAAADnC86AAAHYklEQVR4nLWYW4yVVxXH12Xv7zvnzAxzGIYBZsAZEgltClQQklqqpVSsmhQvMSZt4oNPPnmJ8cXENEYTfKjENjUmNb7gpT4oJlopMViLQWiFIIXCMFJoh2FgBpiZM5dzznfZe6/lw4RE03MZJnE97nxZv7323mut//pQROA+TUEJAUAAQNUA6P16AAC6b6oCIswm+YEjE2dGFxB1OdhlgO/hZWTCv3tbAJZJxmUfdeYDEzLycrDLAwcBACXExVARAPH/D0ZcZP2PqcoHF1ubWfqnogAA82n2r9FEgIioYNga7evSDeVYlQhp6aEvCSyqhMAEADQ8Xv3eH2ZKhSIbjI0V4G0D4UeftwAMgKqiikvBtz9qUWAC0fD2zfTcaLhw3Y1OAjhxOfgMQgaS644h2bvTDPQVH36ghEAhKLVLlzbgoGIIL9xKXjmdXJ0m7wECcI55Kj5Rl6pPIK0Cii8X3YNDtO8R3LFl5ZpVxRACEbW4+FYbE1VDeuSd+edeXRi5Q7HBFR1YKiBaYQtsgSOgWAudaiO6cpM/urXjU4+teeNU5cp7C8zQOr+bgkUDk74+Uvvp8cQaU7TqvXdekdFYNpY4MmzJWEJGNLCmxxw8NP/ujcSF+CvfuluZ89CyqjU+alVA0vFK8p3fVbxGxMpsbVQAEFUfUp/Vg0vE5xgy9TmFlKtzQZyNIfE5jI3iM/vlxef6Q8Bml90YLApMcvDY1F9GfDkmsqU8rY6OnLvx3khSmyckCV6CR2RiTmtZX3nFk7t3X75Wqi1siIldKguV/Pcvd+/a2hUCEDW46QbppApMeLfqT7/vYoNoC1M3rpw+9srCxLV1/Z0dhsYmF9R0AhGqal4bHOhEd/3q8Piz+z/96vH3xyd2dRZWOAmHX0t2be1UbRxyg9XFi/n3ZDpT08hGc1M3Tv7pxYWJ4e3b+nZuKn/20U1ffmqbDTMRpJBVdj20autA8ek920qF6MALh57YWeuI/+YllLrw7WHnvWfT+GE3AgMAwK1KcEGZzeVTh9PZUVvQ9au7/vzHo4ODgwWWtb1FV71TjFxfd8fRo69vHBoa6O1wof6Tnx9eW75YSy4VO0p353RmThAaP++mrzp1HojT+dnK9dMlC5LOJ1n+5L49L73ws+nKfJbUI3IuWVDQjz/26MEfv1SZrzH6hfmZN04c99l5E3FQyFwz9y3yGEFFkZmR89oMaf6Pk29FxdIjj+++MHxlavImSqqueuLkm929PTt37zp7/p3Z6duW8yyrkYmMBbbawn3TWq1KGgJHpS2f+fbVU78OLgWlv5+fJEJjeroHVgcXIgAn4bU3x+KIDfatWrc+eNe3Ycu6oc+5pG4sY/M8bgomUiAJebZyw7aPPfM8+IwMMzMAIUj/GrNiBXcVaHUX3bien72sGjSr+5BicHFey4PzlpG5acgNwIu9ZWiVIVVFlCz1REgqwasqggkY9pfybZmr3wnF2eSX2B3iLk6FDSirc3VjIUFcu5p6y4s+lgxW1Z2DnYO9s+MzrqtoggICgaqKIomi+e1b6fTFmyur7lJ/+cyOQikS71EsiRcrrKTptH/6CWsN+qDcqIC0qFx6bmzhu4fvZt52Fi0TIQKgEBIBB8tMGgXIYo5UIYBPNaTgM0jrYWoq7HkQDnytxxoC4IaJ3LQtqioRXLpV/cWJ2ZFJyT0yUyEiYiJCAgRCZGIFYiIi8ZrUJJnXEsonH6KvPtVVjCKRpnKsVT8WBSYE8FfvZLVcMi/jk847BURARIDgQYEWRVhQ7SzC5oF47UpTLjEAibSSIm2EgCioqmEcm6j98OXKxWFwdfQZgiNFFVEFBAVE0ABRye//kv36syvKxeK9vTW1NpoLAYjh8Jmp538zX7ltIqZg0Xv1uYYUISAgKCoIcAF4R3xsTh4fr+/caDqjWEFbkFuBVYEIZxN36GSVSrx2EPIq+ERcAiEVl1Coo+QgAOqhox+6P4ShhoKmnvuuOGotedurzNxLoWA7e0RSQQaMlSKQCDgKLiapg0/B5Sge0UM1g2t3w8P9eq/XNCW3B0cWI4sckTXAsXACLkZfUKwDR+oi4BSBRBW9mMjyX0eyT3w47u2i5R/14nYNUWSVmYkJWcgEioUj4khDLJRAiAGZoAhBAIkm5rCj0H6gah8xAhhCZiaQxUQiVmODi0Vi5JhcqmRFiEExyWVTv+nvLqhqo3p1P2DLaIhVwbACAhOGgEiIHEKkVBBKkCMNXvIc5pKwd3PESD5o8wYB0FpXI0AQjZi3DsS5D9/YW1rfzV45iogZDRsbcdxBhW4t9aAtBuvS7QPyxe0d0i5caFtAFAAR55J8dNp9ZH3p7Fj1B0fqgGRZVEFFRDSIVqr5xjJ+/wu9vd1Rd8GKth8dlzSmIgoABREmPXG1/qt/JpML4L0GAVBhCg/0wTf39Q72FAF0KdSlgnWxmOBiSYFa7kZuZ5Wa+qCWaaCMm9fGCDaIIi51TL7vwXxxePyvLSEAigYFpPuZzZf3DwRUF0WrIgAgtn1KH7T/AOPRGfhIBxabAAAAAElFTkSuQmCC'
        elif "." in thumbnail:thumbnail = str(Robot_Rubika._getThumbInline(open(file,"rb").read() if not "http" in file else get(file).content))

        if size == []: size = encoder_photo.getThumbInline(open(file,"rb").read() if not "http" in file else get(file).content)

        file_inline = {
            "dc_id": uresponse[0]["dc_id"],
            "file_id": uresponse[0]["id"],
            "type":"Image",
            "file_name": file.split("/")[-1],
            "size": str(len(get(file).content if "http" in file else open(file,"rb").read())),
            "mime": file.split(".")[-1],
            "access_hash_rec": uresponse[1],
            "width": size[0],
            "height": size[1],
            "thumb_inline": thumbnail
        }

        inData = {
                "method":"sendMessage",
                "input":{
                    "file_inline": file_inline,
                    "object_guid": chat_id,
                    "rnd": f"{randint(100000,999999999)}",
                    "reply_to_message_id": message_id
                },
                "client": clien.web
            }
        if caption != None: inData["input"]["text"] = caption

        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.b,self.Auth,inData))).get("data_enc")))
                break
            except: continue

    def sendMusic(self, chat_id, file, time, caption=None, message_id=None):
        uresponse = Robot_Rubika._uploadFile(self, file)
        file_id = str(uresponse[0]["id"])
        mime = file.split(".")[-1]
        dc_id = uresponse[0]["dc_id"]
        access_hash_rec = uresponse[1]
        file_name = file.split("/")[-1]
        size = str(len(get(file).content if "http" in file else open(file,"rb").read()))

        inData = {
                "method":"sendMessage",
                "input":{
                    "file_inline": {
                        "dc_id": dc_id,
                        "file_id": file_id,
                        "type":"Music",
                        "music_performer":"",
                        "file_name": file_name,
                        "size": size,
                        "time": time,
                        "mime": mime,
                        "access_hash_rec": access_hash_rec,
                    },
                    "object_guid":chat_id,
                    "rnd":f"{randint(100000,999999999)}",
                    "reply_to_message_id":message_id
                },
                "client": clien.android
            }

        if caption != None: inData["input"]["text"] = caption


        while 1:
            try:
                loop = asyncio.get_event_loop()
                return loads(self.enc.decrypt(loads(loop.run_until_complete(http(Robot_Rubika.b,self.Auth,inData))).get("data_enc")))
                break
            except: continue
