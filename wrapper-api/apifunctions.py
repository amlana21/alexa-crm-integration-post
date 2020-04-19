import requests
import json
import os
from dotenv import load_dotenv

if os.getenv('ENV')!='PROD':
    load_dotenv()

class apiFunctions:

    def __init__(self,baseurl,authvalues,loginparams):
        self.baseurl=baseurl
        self.authvalues=authvalues
        self.logtkn=self.getLogin(loginparams)



    def getLogin(self,loginparams):
        outTkn={}
        dataBody={'username':self.authvalues['username'],'password':self.authvalues['password'],'grant_type':self.authvalues['grant_type'],
                  'client_id':self.authvalues['client_id'],'client_secret':self.authvalues['client_secret']}
        print(dataBody)
        loginUrl=self.baseurl+'/'+loginparams
        resp = requests.post(loginUrl, data=dataBody)
        if resp.status_code==200:
            outTkn=json.loads(resp.text)
        else:
            raise Exception(resp.text)
        return outTkn

    def queryAll(self,objectname,urlparam,query):
        envurl=self.logtkn["instance_url"]
        qryurl=f'{envurl}/{urlparam}?q={query}'
        print(qryurl)
        hdrs={'Authorization':f'Bearer {self.logtkn["access_token"]}'}
        resp=requests.get(qryurl,headers=hdrs)
        resp_dict={}
        resp_dict=resp.json()
        if resp.status_code==200:
            return resp_dict
        else:
            raise Exception(resp.text)


    def createRecord(self,objectname,urlparam,data):
        envurl = self.logtkn["instance_url"]
        posturl=f'{envurl}/{urlparam}/{objectname}'
        headers={'Authorization':f'Bearer {self.logtkn["access_token"]}','Content-Type':'application/json'}
        resp=requests.post(posturl,data=json.dumps(data),headers=headers)
        print(resp.status_code)
        if resp.status_code==201:
            return resp.json()
        else:
            raise Exception(resp.json())
        # return resp.json()


if __name__=='__main__':
    pass

