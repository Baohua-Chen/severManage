#!/usr/bin/python
# coding: utf-8
# This script can be imported to athour scripts in order to send micromessages to MSG acconts(default Chenbaohua)
import urllib,urllib2
import json
import sys

def gettoken(corpid='wwa3a619ecdbd93753',corpsecret='RhbEl-I6OKulujiTbH39povVoZnAb4U-ltcsyEwn2gE'):
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + corpsecret
    try:
        token_file = urllib2.urlopen(gettoken_url)
#    except urllib2.HTTPError as e:
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

def senddata(access_token,content="Null",user="Chenbaohua"):
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
    send_values = {
        "touser":user,    #企业微信中的用户帐号
        "toparty":"0",    #企业微信中的部门id
        "msgtype":"text",  #消息类型。
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
        user = "Chenbaohua"
    if len(sys.argv)>1:
        content = str(sys.argv[1])
    else:
        content = "Null"
    corpid = 'wwa3a619ecdbd93753'   #CorpID是企业微信的标识
    corpsecret = 'RhbEl-I6OKulujiTbH39povVoZnAb4U-ltcsyEwn2gE'  #corpsecretSecret是管理组凭证密钥
    accesstoken = gettoken(corpid,corpsecret)
    senddata(accesstoken,content,user)
