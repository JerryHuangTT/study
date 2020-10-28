from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from get_sensor import read_sensor

app = Flask('jerry')
api = Api(app)

class Vuser(Resource):
    def get(self, para):
        return {'msg':'','code':0,'data':para}

    def put(self, para):
        body = request.json
        return {'para': para,'body':body}

class Vdevice(Resource):
    def get(self):
        data = read_sensor(request.args.get('count'),
                            request.args.get('index'))
        return {'msg':'','code':0,'data':data}

    def put(self, para):
        body = request.json
        return {'para': para,'body':body}

api.add_resource(Vuser, '/user/<string:para>')
api.add_resource(Vdevice, '/device/jerry')
CORS(app, supports_credentials=True)

#https://127.0.0.1:8090/device/jerry?index=1&count=50
app.run(debug=True, 
        host='0.0.0.0', 
        port=8090,
        ssl_context='adhoc')
'''

from gevent import pywsgi 
server = pywsgi.WSGIServer(('0.0.0.0', 8090), app)
server.serve_forever()
'''