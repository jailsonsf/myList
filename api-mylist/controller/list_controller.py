import datetime
import os

from flask import jsonify, request
from error_handler import error

from model.list import List
from database import db


def get_lists_by_user(id_user):
    return jsonify(db.read("lists", "id_user", id_user))


def get_list(id_list):
    return jsonify(db.read("lists", "id", id_list))


def create_list():
    json = request.get_json()

    id = db.create_id("lists")
    title = json["title"]
    id_user = json["id_user"]

    if not db.verify_register("users", "id", id_user):
        return jsonify(error(400, "User not exists"))
    elif db.verify_register("lists", "id", id):
        return jsonify(error(400, "List already exists"))
    else:
        # create instance
        list_user = List(id, id_user, title, datetime.datetime.utcnow())

        # insert into database
        if db.insert("lists", list_user.to_dict()):
            return jsonify(list_user.to_dict())
        else:
            return jsonify(error(203, "Not Allowed"))


def update_list(id_list):
    if request.method == "POST":
        # query for check username
        query_db = db.read("lists", "id", id_list)
        list_user = query_db[0] if len(query_db) == 1 else None
        if list_user == None:
            return jsonify(error(404, "List not exists"))

        else:
            json = request.get_json()

            id = list_user["id"]
            title = json["title"]
            date = list_user["date"]
            id_user = list_user["id_user"]
            link = list_user["link"]

            list_user = List(id, id_user, title, date)

            if db.update("lists", id_list, list_user.to_dict()):
                return jsonify(list_user.to_dict())

            else:
                return jsonify(error(203, "Not Allowed"))


def delete_list(id_list):
    if request.method == "DELETE":
        # query for check list
        query_db = db.read("lists", "id", id_list)
        list_user = query_db[0] if len(query_db) == 1 else None
        if list_user == None:
            return jsonify(error(404, "List not exists"))

        else:
            if db.delete("lists", id_list):

                # delete all tasks
                tasks = db.read("tasks", "id_list", id_list)
                if len(tasks) > 0:
                    for task in tasks:
                        db.delete("tasks", task["id"])

                return jsonify(error(200, "Removed"))

            else:
                return jsonify(error(400, "Not removed"))
