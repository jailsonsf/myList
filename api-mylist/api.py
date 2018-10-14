'''
    API RestFul
    Start at 12/10/2018 10:58 
'''
from flask import Flask, jsonify, request, abort 
import firebase_admin 
from firebase_admin import firestore 
from database import Database
import datetime 
from error_handler import error

# import model 
from model.user import User 
from model.list import List 
from model.task import Task 

# initialize Flask 
app = Flask(__name__)

# initialize database 
db = Database(firebase_admin, firestore)

# routes user 
@app.route('/users/<usarname>', methods=['GET', 'UPDATE', 'DELETE'])
def get_user(usarname):
    if request.method == 'GET':
        return jsonify(db.read('users', 'username', usarname))

    
@app.route('/users', methods=['POST'])
def create_user():
    if request.method == 'POST':
        print("Requisição feita")

        json = request.get_json()

        id = db.create_id('users')
        username = json['username']
        name = json['name']
        email = json['email']

        if (db.verify_register('users', 'username', username)):
            return jsonify(error(400, 'Username already exists'))
        else:
            # create instance 
            user = User(id, username, name, email, datetime.datetime.utcnow())

            # insert into database 
            if(db.insert('users', user.to_dict())):
                return jsonify(user.to_dict())
            else:
               return jsonify(error(203, 'Not Allowed'))
    else:
        return jsonify(error(405, 'Method has to be POST'))

@app.route('/users/<id_user>', methods=['POST'])
def update_user(id_user):
    if request.method == 'POST':
        # query for check username 
        query_db = db.read('users', 'id', id_user)
        user = query_db[0] if len(query_db) == 1 else None 
        if(user == None):
            return jsonify(error(404, 'User not exists'))
        
        else:
            json = request.get_json()

            username = json['username']
            name = json['name']
            email = json['email']
            date = user['date_creation']

            if (user['username'] != username and db.verify_register('users', 'username', username)):
                return jsonify(error(400, 'User invalid or user already exists'))

            else:
                user = User(id_user, username, name, email, date)
                
                if(db.update('users', id_user, user.to_dict())):
                    return jsonify(user.to_dict())
                
                else:
                    return jsonify(error(203, 'Not Allowed'))
    else:
        return jsonify(error(405, 'Method has to be POST'))

            


    # @app.route('/users/<int:id_user>', method=('DELETE'))
    # def delete_user(id_user):
    #     db.delete('users', id_user)
    
    # @app.route('/lists/<int:id_list>', method=['GET'])
    # def get_list(id_list):
    #     if request.method == "GET":
    #         return jsonify([db.read('lists', id_list)])
        



