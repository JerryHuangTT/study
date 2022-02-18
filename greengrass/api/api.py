from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
#from get_infer import read_sensor
import os
from werkzeug.utils import secure_filename

app = Flask('jerry')
app.config['UPLOAD_FOLDER'] = 'C:\\jerry\\code\\study\\upload'
api = Api(app)

class Vuser(Resource):
    def get(self,para):
        return {'msg':'','code':0,'data':1}

    # def get(self, para):
    #     return {'msg':'','code':0,'data':para}

    def put(self, para):
        body = request.json
        return {'para': para,'body':body}

    def post(self, para):
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        a = request.form['model_name']
        print(a)
        return {'para': para,'body':'1'}

class Vdevice(Resource):
    def get(self):
        data =0
        # data = read_sensor(int(request.args.get('index')),
        #                     int(request.args.get('count')))                     
        return {'msg':'', 'code':len(data), 'data':data}

    def put(self, para):
        body = request.json
        return {'para': para,'body':body}

api.add_resource(Vuser, '/user/<string:para>')#/<string:para>')
api.add_resource(Vdevice, '/device/jerry')
CORS(app, supports_credentials=True)

#https://127.0.0.1:8090/device/jerry?index=1&count=50
app.run(debug=False, 
        host='0.0.0.0', 
        port=8090,
        ssl_context='adhoc')
        

# from gevent import pywsgi 
# server = pywsgi.WSGIServer(('0.0.0.0', 8090), app)
# server.serve_forever()