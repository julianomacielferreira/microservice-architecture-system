"""
The MIT License

Copyright 2025 Juliano Maciel.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from validate_service import validate_jwt
from login_service import Authenticator
from uploader import upload_video_to_mongodb

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server)

mongoGridFS = gridfs.GridFS(mongo.db)

# connection with rabbitmq synchronous
connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
rabbitmq_channel = connection.channel()

authenticator = Authenticator(os.environ.get("AUTH_SERVICE_URL"))


@server.route("/login", methods=["POST"])
def login():
    token, error = authenticator.login(request)

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
            error = upload_video_to_mongodb(file, mongoGridFS, rabbitmq_channel, payload)

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
    # this tells the operational system to listen to all public IPs
    server.run(host="0.0.0.0", port=8080)
