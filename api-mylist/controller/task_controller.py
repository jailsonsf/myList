import datetime
import os

from flask import jsonify, request
from error_handler import error

from model.task import Task
from database import db


def get_task(id_task):
    return jsonify(db.read("tasks", "id", id_task))


def get_tasks_by_list(id_list):
    return jsonify(db.read("tasks", "id_list", id_list))


def create_task():
    json = request.get_json()

    id = db.create_id("tasks")
    title = json["title"]
    description = json["description"]
    id_list = json["id_list"]

    if not db.verify_register("lists", "id", id_list):
        return jsonify(error(400, "List not exists"))
    elif db.verify_register("tasks", "id", id):
        return jsonify(error(400, "Task already exists"))
    else:
        # create instance
        task = Task(id, id_list, title, description, datetime.datetime.utcnow())

        # insert into database
        if db.insert("tasks", task.to_dict()):
            return jsonify(task.to_dict())
        else:
            return jsonify(error(203, "Not Allowed"))


def update_task(id_task):

    if request.method == "POST":

        # query for check id task
        query_db = db.read("tasks", "id", id_task)
        task = query_db[0] if len(query_db) == 1 else None
        if task == None:
            return jsonify(error(404, "Task not exists"))

        else:
            json = request.get_json()

            id = task["id"]
            title = json["title"]
            description = json["description"]
            date = task["date"]
            id_list = task["id_list"]
            status = json["status"]

            task = Task(
                id=id,
                id_list=id_list,
                title=title,
                description=description,
                date=date,
                status=status,
            )

            if db.update("tasks", id_task, task.to_dict()):
                return jsonify(task.to_dict())

            else:
                return jsonify(error(203, "Not Allowed"))


def delete_task(id_task):
    if request.method == "DELETE":
        # query for check task
        query_db = db.read("tasks", "id", id_task)
        task = query_db[0] if len(query_db) == 1 else None
        if task == None:
            return jsonify(error(404, "Task not exists"))

        else:
            if db.delete("tasks", id_task):

                return jsonify(error(200, "Removed"))

            else:
                return jsonify(error(400, "Not removed"))
