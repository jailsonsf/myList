import datetime
import os

from flask import jsonify, request
from error_handler import error

# import model
from model.user import User
from database import db


def get_user(username):
    return jsonify(db.read("users", "username", username))


def create_user():
    json = request.get_json()

    id = db.create_id("users")
    username = json["username"]
    name = json["name"]
    email = json["email"]

    if db.verify_register("users", "username", username):
        return jsonify(error(400, "Username already exists"))
    else:
        # create instance
        user = User(id, username, name, email, datetime.datetime.utcnow())

        # insert into database
        if db.insert("users", user.to_dict()):
            return jsonify(user.to_dict())
        else:
            return jsonify(error(203, "Not Allowed"))


def update_user(id_user):
    if request.method == "POST":
        # query for check username
        query_db = db.read("users", "id", id_user)
        user = query_db[0] if len(query_db) == 1 else None
        if user == None:
            return jsonify(error(404, "User not exists"))

        else:
            json = request.get_json()

            username = json["username"]
            name = json["name"]
            email = json["email"]
            date = user["date_creation"]

            if user["username"] != username and db.verify_register(
                "users", "username", username
            ):
                return jsonify(error(400, "User invalid or user already exists"))

            else:
                user = User(id_user, username, name, email, date)

                if db.update("users", id_user, user.to_dict()):
                    return jsonify(user.to_dict())

                else:
                    return jsonify(error(203, "Not Allowed"))


def delete_user(id_user):
    if request.method == "DELETE":
        # query for check username
        query_db = db.read("users", "id", id_user)
        user = query_db[0] if len(query_db) == 1 else None
        print("ola")
        if user == None:
            return jsonify(error(404, "User not exists"))

        else:

            if db.delete("users", id_user):

                # delete all lists
                lists = db.read("lists", "id_user", id_user)

                if len(lists) > 0:
                    for list_user in lists:
                        print(list_user["id"])
                        db.delete("lists", list_user["id"])

                return jsonify(error(200, "Removed"))

            else:
                return jsonify(error(400, "Not removed"))


def get_lists_by_user(id_user):
    return jsonify(db.read("lists", "id_user", id_user))
