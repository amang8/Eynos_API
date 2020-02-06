from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister, AllUsers, FollowUser

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'abcde'
api = Api(app)

# create an auth endpoint
jwt = JWT(app, authenticate, identity)

api.add_resource(AllUsers, '/allusers')
api.add_resource(UserRegister, '/register')
api.add_resource(FollowUser, '/follow_user')


if __name__ == '__main__':
    app.run(debug=True)