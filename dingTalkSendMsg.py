#!/public/softwares/miniconda3/bin/python3

from configparser import ConfigParser
import time
import json
import socket
import os
from urllib import request
import sys


class myConfigParser(ConfigParser):
	"""
	set ConfigParser options for case sensitive.
	"""
	def __init__(self, defaults=None):
		ConfigParser.__init__(self, defaults=defaults)
 
	def optionxform(self, optionstr):
		return optionstr

def getToken(key, secret):
	apiUrl = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' %(key, secret)
	res = request.urlopen(request.Request(apiUrl))
	res = json.load(res)
	token = res['access_token']
	return token

def getIp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def sendMsg(token, agentID, fUsers, template, userNames, *args):
	args = list(zip(*args))
	userIDs =  [ os.popen('grep "' + userName + '" ' + fUsers + ' |head -n 1 |cut -f 2').read().strip() for userName in userNames ]
	hostname = socket.gethostname()
	ip = getIp()
	apiUrl = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=%s' %(token)
	headers = {"Content-Type": "application/json", "Charset": "UTF-8"}
	lt = []
	for i in range(len(userNames)):
		try:
			msg = template.format(*args[i])
		except IndexError:
			msg = template
		cont = '%s\n_____________________\nSend by %s\n\tIP: %s\n\t%s\n' %(msg, hostname, ip, time.strftime("\n%Y-%m-%d %H:%M:%S", time.localtime()))
		if userIDs[i] != '':
			data = {
				'msg' : {
					'msgtype' : 'text',
					'text':{
						'content' : cont
						}
					},
				'agent_id' : agentID,
				'userid_list' : userIDs[i]
				}
			req = request.Request(url=apiUrl, data=json.dumps(data).encode('utf-8'),  headers=headers, method='POST')
			res = json.load(request.urlopen(req))
			lt.append(res)
		else:
			print('Can not find user ' + userNames[i])
			lt.append(None)
	return lt

if __name__ == '__main__':
	cfgParser = myConfigParser()
	cfgParser.read_file(open(os.environ['HOME']+'/.dingding/dingding.cfg'))
	appKey = cfgParser.get('APP', 'appKey')
	appSecret = cfgParser.get('APP', 'appSecret')
	agentID = cfgParser.getint('APP', 'agentID')
	fUsers = cfgParser.get('users', 'fUsers')

#	userList = ['陈葆华', '陈葆华']
	userList = sys.argv[1].split(',')
#	template = 'Dear {:s},\n\t this is the {:s} message.'
	template = sys.argv[2].replace('\\n', '\n').replace('\\t', '\t')
	extraArgs = [ i.split(',') for i in sys.argv[3:] ]
	token = getToken(appKey, appSecret)
	res = sendMsg(token, agentID, fUsers, template, userList, *extraArgs)
	for i in res:
		print(i)

