from model.user import User
from model.task import Task
from model.list import List
import requests
import json

URL_CREATE_USER = 'https://api-milyst.herokuapp.com/users'
URL_CREATE_TASK = 'https://api-milyst.herokuapp.com/tasks'
URL_CREATE_LIST = 'https://api-milyst.herokuapp.com/lists'

URL_DEL_USER = 'https://api-milyst.herokuapp.com/users/delete'
URL_DEL_TASK ='https://api-milyst.herokuapp.com/tasks/delete'
URL_DEL_LIST = 'https://api-milyst.herokuapp.com/lists/delete'

URL_GET_USER = 'https://api-milyst.herokuapp.com/users/'
URL_GET_TASK = 'https://api-milyst.herokuapp.com/tasks/'
URL_GET_LIST = 'https://api-milyst.herokuapp.com/lists/'

def create_user(user):

    jsonArray = json.dumps(user.to_dict())
    response = requests.post(URL_CREATE_USER, data = jsonArray)

    return json.loads(response.content)

def create_task(task):

    jsonArray = json.dumps(task.to_dict())
    response = requests.post(URL_CREATE_TASK, data = jsonArray)

    return json.loads(response.content)

def create_list(list):

    jsonArray = json.dumps(list.to_dict())
    response = requests.post(URL_CREATE_LIST, data = jsonArray)

    return json.loads(response.content)

if __name__ == '__main__':

    # login

    user = User(1, 'lulu', 'luis', 'lulu@gmail.com', '11/11/2011')
    user = create_user(user)

    # make list

    list_user = List(1, user['id'], 'title', '11/11/2011')
    list_user = create_list(list_user)

    # make task

    task = Task(1, list_user['id'], list_user['title'], 'description', '11/11/2011', 'status')
    task = create_task(task)
