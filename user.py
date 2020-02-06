import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import json


class User:
    TABLE_USER = 'users'
    TABLE_FOLLOWER = 'followers'

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE username=?".format(table=cls.TABLE_USER)
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_USER)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    TABLE_USER = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES (NULL, ?, ?)".format(table=self.TABLE_USER)
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201


class AllUsers(Resource):
    TABLE_USER = 'users'

    @jwt_required()
    def get(self):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_USER)
        results = cursor.execute(query)

        output = []
        if results:
            for result in results:
                output.append({'id': result[0], 'name': result[1]})

        connection.close()
        return {'users_list' : output}


class FollowUser(Resource):
    TABLE_FOLLOWER = 'followers'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required
    def post(self):
        data = FollowUser.parser.parse_args()
        logged_user = current_identity
        results = FollowUser.get_follower(logged_user)
        if results:
            for result in results:
                if safe_str_cmp(result['name'], data['username']):
                    return {'message': 'Already following'}, 200

            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "INSERT INTO {table} VALUES (NULL, ?, ?)".format(table=self.TABLE_FOLLOWER)
            input(query)
            cursor.execute(query, (logged_user, data['username']))

            connection.commit()
            connection.close()
            return {'message': 'Success'}, 201
        else:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "INSERT INTO {table} VALUES (NULL, ?, ?)".format(table=self.TABLE_FOLLOWER)
            input(query)
            cursor.execute(query, (logged_user, data['username']))

            connection.commit()
            connection.close()
            return {"message": "Success"}, 201

    @classmethod
    def get_follower(cls, user):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE username = ?".format(table=cls.TABLE_FOLLOWER)
        results = cursor.execute(query, (user, ))
        output = []
        if results:
            for result in results:
                output.append({'name': result[2]})

        connection.close()
        input(output)
        return output



