'''
    API RestFul
    Start at 12/10/2018 10:58 
'''
from flask import Flask, jsonify, request, abort 
from firebase_admin import firestore 
from error_handler import error
from database import Database
import firebase_admin 
import datetime 
import os

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
    return jsonify(db.read('users', 'username', usarname))
    
@app.route('/users', methods=['POST'])
def create_user():
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

@app.route('/users/<id_user>', methods=['POST'])
def update_user(id_user):
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

@app.route('/users/delete/<id_user>', methods=['DELETE'])
def delete_user(id_user):
    # query for check username 
    query_db = db.read('users', 'id', id_user)
    user = query_db[0] if len(query_db) == 1 else None 
    if (user == None):
        return jsonify(error(404, 'User not exists'))
    
    else:

        if (db.delete('users', id_user)):
            
            # delete all lists
            lists = db.read('lists', 'id_user', id_user)

            if (len(lists) > 0):
                for list_user in lists:
                    print(list_user['id'])
                    db.delete('lists', list_user['id'])

            return jsonify(error(200, "Removed"))

        else:
            return jsonify(error(400, "Not removed"))    

@app.route('/users/lists/<id_user>', methods=['GET'])
def get_lists_by_user(id_user):
    return jsonify(db.read('lists', 'id_user', id_user))

@app.route('/lists/<id_list>', methods=['GET'])
def get_list(id_list):
    return jsonify(db.read('lists', 'id', id_list))

@app.route('/lists', methods=['POST'])
def create_list():
    json = request.get_json()

    id = db.create_id('lists')
    title = json['title']
    id_user = json['id_user']

    if (db.verify_register('lists', 'id', id)):
        return jsonify(error(400, 'List already exists'))
    else:
        # create instance 
        list_user = List(id, id_user, title, datetime.datetime.utcnow())

        # insert into database 
        if(db.insert('lists', list_user.to_dict())):
            return jsonify(list_user.to_dict())
        else:
            return jsonify(error(203, 'Not Allowed'))
   
@app.route('/lists/delete/<id_list>', methods=['DELETE'])
def delete_list(id_list):
    # query for check list 
    query_db = db.read('lists', 'id', id_list)
    list_user = query_db[0] if len(query_db) == 1 else None 
    if (list_user == None):
        return jsonify(error(404, 'List not exists'))
    
    else:
        if (db.delete('lists', id_list)):
            
            # delete all tasks 
            tasks = db.read('tasks', 'id_list', id_list)
            if (len(tasks) > 0):
                for task in tasks:
                    db.delete('tasks', task['id'])

            return jsonify(error(200, "Removed"))

        else:
            return jsonify(error(400, "Not removed"))

  

@app.route('/tasks/<id_task>', methods=['GET'])
def get_task(id_task):
    return jsonify(db.read('tasks', 'id', id_task))

@app.route('/lists/tasks/<id_list>', methods=['GET'])
def get_tasks_by_list(id_list):
    return jsonify(db.read('tasks', 'id_list', id_list))

@app.route('/tasks', methods=['POST'])
def create_task():
    json = request.get_json()

    id = db.create_id('tasks')
    title = json['title']
    description = json['description']
    id_list = json['id_list']

    if (db.verify_register('task', 'id', id)):
        return jsonify(error(400, 'Task already exists'))
    else:
        # create instance 
        task = Task(id, id_list, title, description, datetime.datetime.utcnow())

        # insert into database 
        if(db.insert('tasks', task.to_dict())):
            return jsonify(task.to_dict())
        else:
            return jsonify(error(203, 'Not Allowed'))

@app.route('/tasks/delete/<id_task>', methods=['DELETE'])
def delete_task(id_task):
    # query for check task 
    query_db = db.read('tasks', 'id', id_task)
    task = query_db[0] if len(query_db) == 1 else None 
    if (task == None):
        return jsonify(error(404, 'Task not exists'))
    
    else:
        if (db.delete('tasks', id_task)):

            return jsonify(error(200, "Removed"))

        else:
            return jsonify(error(400, "Not removed"))

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='127.0.0.1', port=port)
        



