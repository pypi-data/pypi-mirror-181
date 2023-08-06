from flask_restful import Api, Resource, reqparse
from maxmods.auth.imports import *

session = Session()
api = Api(session.app)

Dataargs = reqparse.RequestParser()
Dataargs.add_argument('location', type=str)
Dataargs.add_argument('data', type=str)
Dataargs.add_argument('username', type=str)
Dataargs.add_argument('password', type=str)
Dataargs.add_argument('hash', type=str)
Dataargs.add_argument('id', type=str)
        
class Load(Resource):
    def post(self):#load data
        data = Dataargs.parse_args()
        
        return session.post('load_data', None, {'location':data['location'], 'hash':data['hash'], 'id':data['id']}, verify=True).json()

class Save(Resource):
    def post(self):#save data
        data = Dataargs.parse_args()

        return session.post('save_data', None, {'location':data['location'], 'data':data['data'], 'hash':data['hash'], 'id':data['id']}, verify=True).json()

class Remove(Resource):
    def post(self):#remove user
        data = Dataargs.parse_args()
        
        return session.post('remove_account', None, {'hash':data['hash'], 'id':data['id']}, verify=True).json()

class Login(Resource):
    def post(self):#login
        data = Dataargs.parse_args()
        
        return session.post('log_in', None, {'username':data['username'], 'password':data['password'], 'hash':data['hash'], 'id':data['id']}, verify=True).json()
        
class Signup(Resource):
    def post(slef):#signup
        data = Dataargs.parse_args()
        
        return session.post('sign_up', None, {'username':data['username'], 'password':data['password']}, verify=True).json()

class Greet(Resource):
    def post(self):#greeting
        data = Dataargs.parse_args()

        return session.post('create_session', None, {'id':data['id']}, verify=True).json()

class Leave(Resource):
    def post(self):#goodbyes
        data = Dataargs.parse_args()
        
        return session.post('end_session', None, {'hash':data['hash'], 'id':data['id']}, verify=True).json()

class Delete(Resource):
    def post(self):
        data = Dataargs.parse_args()
        
        return session.post('delete_data', None, {'location':data['location'], 'hash':data['hash'], 'id':data['iD']}, verify=True).json()

class Cert(Resource):
    def post(slef):
        with open('server-public-key.pem') as f:
            serv = f.read()
        
        return {'code':102, 'server': serv}

class Logout(Resource):
    def post(self):
        data = Dataargs.parse_args()
        
        return session.post('log_out', None, {'hash':data['hash'], 'id':data['id']}, verify=True).json()

api.add_resource(Login, '/log_in')
api.add_resource(Signup, '/sign_up')
api.add_resource(Greet, '/create_session')
api.add_resource(Leave, '/end_session')
api.add_resource(Load, '/load_data')
api.add_resource(Save, '/save_data')
api.add_resource(Remove, '/remove_account')
api.add_resource(Delete, '/delete_data')
api.add_resource(Cert, '/Cert')
api.add_resource(Logout, '/log_out')

def start_server(host = None, port = None):
    if not os.path.isfile('server-public-key.pem') or not os.path.isfile('server-private-key.pem'):
        from maxmods.auth.auth_backend import cert_maker
    session.app.run(host=host, port=port, ssl_context=('server-public-key.pem', 'server-private-key.pem'))
if __name__ == '__main__':
    start_server('0.0.0.0', 5678)