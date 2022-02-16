#!/usr/bin/python
# coding: utf-8
# This script can be imported to athour scripts in order to send micromessages to MSG acconts.
import urllib,urllib2
import json
import sys

def gettoken(corpid, corpsecret):
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + corpsecret
    try:
        token_file = urllib2.urlopen(gettoken_url)
    except Exception, e:
        print "Send micro messege faild."
        print e.reason
        return "wrong token"
    else:
        token_data = token_file.read().decode('utf-8')
        token_json = json.loads(token_data)
        token_json.keys()
        token = token_json['access_token']
        return token

def senddata(access_token, user, content="Null"):
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
    send_values = {
        "touser":user,    #User ID
        "toparty":"0",    #Comany ID
        "msgtype":"text",  #Message type
        "agentid":"1000002",
        "text":{
            "content":content
           },
        "safe":"0"
        }
    send_data = json.dumps(send_values, ensure_ascii=False)
    try:
        send_request = urllib2.Request(send_url, send_data)
    except Exception,e:
        print e.reason
    else:
        try:
            response = json.loads(urllib2.urlopen(send_request).read())
        except Exception,e:
            print e.reason
        else:
            print str(response)



if __name__ == '__main__':
    if len(sys.argv)>2:
        user = str(sys.argv[2])
    else:
        user = "chenbaohua"
    if len(sys.argv)>1:
        content = str(sys.argv[1])
    else:
        content = "Null"
    corpid = 'xxxx'   #Corporation ID
    corpsecret = 'xxxxxxxxxxxxxxxx'  #Authen of administrators
    accesstoken = gettoken(corpid, corpsecret)
    senddata(accesstoken, user, content)
