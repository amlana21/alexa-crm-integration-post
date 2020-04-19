import os,base64
from dotenv import load_dotenv
from flask import Flask,render_template,make_response,jsonify,request
from apifunctions import apiFunctions


if os.getenv('ENV')!='PROD':
    load_dotenv()

app=Flask(__name__)


@app.route('/')
def index():
    return 'aaa'

@app.route('/getall')
def queryAll():
    args=request.args
    resp=None

    # print(usrName)
    try:
        authHdr = request.headers['Authorization']
        print(authHdr)
        authStr = base64.b64decode(authHdr.split(' ')[1]).decode("utf-8").split(':')
        print(authStr)
        usrName = authStr[0]
        psswrd = authStr[1]
        urlparams=request.headers['urlparams']
        authDict = {'username': usrName, 'password': psswrd,
                'grant_type': os.getenv('GRANTTYPE'), 'client_id': os.getenv('CLIENTID'),
                'client_secret': os.getenv('CLIENTSECRET')}
        apiobj = apiFunctions(os.getenv('HOSTURL'), authDict, 'services/oauth2/token')
        dataresp=apiobj.queryAll('lead',urlparams,args['q'])
        resp=make_response(jsonify(data=dataresp),200)
    except Exception as e:
        resp=make_response(jsonify(error=str(e)),500)
    return resp

@app.route('/createrecord/<objectname>',methods=['POST'])
def createRecord(objectname):
    resp=None
    try:
        authHdr = request.headers['Authorization']
        authStr = base64.b64decode(authHdr.split(' ')[1]).decode("utf-8").split(':')
        usrName = authStr[0]
        psswrd = authStr[1]
        inputbody={}
        inputbody=request.get_json()
        if (not inputbody) or len(inputbody)==0:
            raise Exception('No input body found!!')
        authDict = {'username': usrName, 'password': psswrd,
                'grant_type': os.getenv('GRANTTYPE'), 'client_id': os.getenv('CLIENTID'),
                'client_secret': os.getenv('CLIENTSECRET')}
        apiobj = apiFunctions(os.getenv('HOSTURL'), authDict, 'services/oauth2/token')
        createresp=apiobj.createRecord(objectname,inputbody['urlparams'],inputbody['data'])
        resp=make_response(jsonify(data=createresp),200)
    except Exception as e:
        resp=make_response(jsonify(error=str(e)),500)
    return resp

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')