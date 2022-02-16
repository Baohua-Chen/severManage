#!/home/bin/python3

import json
from urllib import request
import pandas as pd

def getToken(key, secret):
    apiUrl = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' %(key, secret)
    res = request.urlopen(request.Request(apiUrl))
    res = json.load(res)
    token = res['access_token']
    return token

def getDeptList():
    apiUrl = 'https://oapi.dingtalk.com/department/list?access_token=%s' %(token)
    res = request.urlopen(request.Request(apiUrl))
    res = json.load(res)
    res = pd.DataFrame(res['department']).set_index('id')['name'].to_dict()
    return res

def getUsers(deptList):

    def perDept(deptID):
        apiUrl = 'https://oapi.dingtalk.com/user/getDeptMember?access_token=%s&deptId=%d' %(token, deptID)
        res = request.urlopen(request.Request(apiUrl))
        res = json.load(res)
        res = res['userIds']
        return res

    def getDetail(userID):
        apiUrl = 'https://oapi.dingtalk.com/user/get?access_token=%s&userid=%s' %(token, userID)
        res = request.urlopen(request.Request(apiUrl))
        res = json.load(res)
        res = res['name']
        return res

    lt = []
    for deptID, deptName in deptList.items():
        for userID in perDept(deptID):
            userName = getDetail(userID)
            lt.append([userName, userID, deptName, deptID])
    d = pd.DataFrame(lt, columns=['userName', 'userID', 'deptName', 'deptID'])
    print(d)
    return d

if __name__ == '__main__':
    appKey='dingqhvo4jhmli4omj7f'
    appSecret='OvLVHDuM6itkrecx9c9dD32UX88Pz2RR_Kjc0RUTw8Zsa-N-vWDwP9i4pbIc0TXx'
    token = getToken(appKey, appSecret)
    deptList = getDeptList()
    userDetails = getUsers(deptList)
    userDetails.to_csv('~/.dingding/userDetails.txt', index=None, sep='\t')

