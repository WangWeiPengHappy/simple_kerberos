# client.py
import requests
import json
#json format
#request
#method: AS, TGS, CS
#message: str info

#response
#key:

KDC_SERVER='http://localhost:8001'
DATA_SERVER='http://localhost:8002'
CLIENT_ID="12345"
g_replyData=""
#common
CLIENT_KEY="CLIENT_KEY"
g_ct_sk=""
g_cs_sk=""


def SendReq(server, msg):
    response = requests.post(server, json=msg)
    print('Response from server:', response.json())
    a = response.json()
    return a

def ASReq():
    msg={'method':'AS', 'basic':CLIENT_ID, 'message':'This is AS'}
    return SendReq(KDC_SERVER, msg)
    

def TGSReq(param):
    if(param==""):
        return
    #verify AS reply
    basic = param['basic']
    if(basic!=CLIENT_KEY):
        return
    
    CT_SK = param['CT_SK']
    global g_ct_sk
    g_ct_sk=CT_SK
    TGT = param['TGT']
    msg={'method':'TGS', 'basic':CT_SK, 'TGT':TGT, 'server':DATA_SERVER}
    return SendReq(KDC_SERVER, msg)

def ServerReq(param):
    if(param==""):
        return
    #verify TGS reply

    basic = param['basic']
    if(basic!=g_ct_sk):
        return
    
    CS_SK=param['CS_SK']
    global g_cs_sk
    g_cs_sk=CS_SK
    ST=param['ST']


    msg={'method':'CS', 'basic':CS_SK, 'ST':ST, 'message':"Hello, I am client A"}
    return SendReq(DATA_SERVER, msg)

def verify_server(param):
    if(param==""):
        return
    CS_SK=param['basic']
    if(CS_SK!=g_cs_sk):
        return False
    return True
    

def Kdcflow():
    ret = ASReq()
    ret=TGSReq(ret)
    ret=ServerReq(ret)

    result = verify_server(ret)
    if(result == False):
        return
    message=ret['message']
    print("Recive server response: ", message)
    return


Kdcflow()

