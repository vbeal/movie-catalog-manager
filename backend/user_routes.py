from flask import request, jsonify
from flask_restful import Resource

class UserList(Resource):
    def __init__(self, db):
        self.db = db

    def get(self):
        users = self.db.users.find()
        return [
            {
                "_id": str(user["_id"]),
                "username": user["username"],
                "email": user.get("email", ""),
                "phone": user.get("phone", ""),
                "role": user.get("role", "common"),
            }
            for user in users
        ]

def initialize_user_routes(app, db):
    @app.route("/users")
    def list_users():
        users = db.users.find()
        return jsonify([
            {
                "_id": str(user["_id"]),
                "username": user["username"],
                "email": user.get("email", ""),
                "phone": user.get("phone", ""),
                "role": user.get("role", "common"),
            }
            for user in users
        ])
