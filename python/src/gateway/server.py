import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from validate_service import validate_jwt
from login_service import auth_login
from uploader import upload_video_to_mongodb

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server)

mongoGridFS = gridfs.GridFS(mongo.db)

# connection with rabbitmq syncronous
connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
rabbitMQChannel = connection.channel()


@server.route("/login", methods=["POST"])
def login():
    token, error = auth_login(request)

    if error:
        return error

    return token


@server.route("/upload", methods=["POST"])
def upload():
    payload, error = validate_jwt(request)

    if error:
        return error

    payload = json.loads(payload)

    if payload["is_admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly 1 file required", 400

        for key, file in request.files.items():
            error = upload_video_to_mongodb(file, mongoGridFS, rabbitMQChannel, payload)

            if error:
                return error

        return "success!", 200
    else:
        return "not authorized.", 401


@server.route("/download", methods=["GET"])
def download():
    pass


# config entry point listening on port 8080
if __name__ == "__main__":
    # this tells the operation system to listen to all public IPs
    server.run(host="0.0.0.0", port=8080)
