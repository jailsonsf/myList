"""
    API RestFul
    Start at 12/10/2018 10:58 
"""
import os

from flask import Flask, jsonify, request, abort

from controller import user_controller, list_controller, task_controller

# initialize Flask
app = Flask(__name__)

# routes user
app.add_url_rule(
    "/users/<username>",
    view_func=user_controller.get_user,
    methods=["GET", "UPDATE", "DELETE"],
)

app.add_url_rule("/users/", view_func=user_controller.create_user, methods=["POST"])

app.add_url_rule(
    "/users/<id_user>", view_func=user_controller.update_user, methods=["POST"]
)

app.add_url_rule(
    "/users/delete/<id_user>", view_func=user_controller.delete_user, methods=["DELETE"]
)

app.add_url_rule(
    "/users/lists/<id_user>",
    view_func=user_controller.get_lists_by_user,
    methods=["GET"],
)

# routes list
app.add_url_rule(
    "/users/lists/<id_user>",
    view_func=list_controller.get_lists_by_user,
    methods=["GET"],
)

app.add_url_rule(
    "/lists/<id_list>", view_func=list_controller.get_list, methods=["GET"]
)


app.add_url_rule("/lists", view_func=list_controller.create_list, methods=["POST"])


app.add_url_rule(
    "/lists/<id_list>", view_func=list_controller.update_list, methods=["POST"]
)


app.add_url_rule(
    "/lists/delete/<id_list>", view_func=list_controller.delete_list, methods=["DELETE"]
)

# routes task
app.add_url_rule(
    "/tasks/<id_task>", view_func=task_controller.get_task, methods=["GET"]
)

app.add_url_rule(
    "/lists/tasks/<id_list>",
    view_func=task_controller.get_tasks_by_list,
    methods=["GET"],
)

app.add_url_rule("/tasks", view_func=task_controller.create_task, methods=["POST"])


app.add_url_rule(
    "/tasks/<id_task>", view_func=task_controller.update_task, methods=["POST"]
)


app.add_url_rule(
    "/tasks/delete/<id_task>", view_func=task_controller.delete_task, methods=["DELETE"]
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
