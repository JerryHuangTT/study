from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask('jerry')
api = Api(app)

class Cuser(Resource):
    def get(self, para):
        body = request.json
        return {'para': para,'body':body}

    def put(self, para):
        body = request.json
        return {'para': para,'body':body}

class Cdevice(Resource):
    def get(self, para):
        body = request.json
        return {'data': [[1603825263714, 0.221930568, -0.21332435, 0.268806992, 0.041505167, 1.063264714, 1.032013765, 0]],'body':body}

    def put(self, para):
        body = request.json
        return {'para': para,'body':body}

api.add_resource(Cuser, '/user/test/<string:para>')
api.add_resource(Cdevice, '/device/<string:para>')
CORS(app, supports_credentials=True)

'''
app.run(debug=False, 
        host='0.0.0.0', 
        port=8080,
        ssl_context='adhoc')
'''

from gevent import pywsgi 
server = pywsgi.WSGIServer(('0.0.0.0', 8080), app)
server.serve_forever()