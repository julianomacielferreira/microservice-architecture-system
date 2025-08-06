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
import os

import pika, json


class VideoUploader:
    """
       Class responsible for uploading videos to MongoDB GridFS and sending a message to RabbitMQ.
    """

    def __init__(self, mongo_gridfs, rabbitmq_channel):
        """
           Initializes the class with MongoDB GridFS and RabbitMQ channel.

           Args:
              mongo_gridfs: MongoDB GridFS instance.
              rabbitmq_channel: RabbitMQ channel instance.
        """
        self.mongo_gridfs = mongo_gridfs
        self.rabbitmq_channel = rabbitmq_channel

    def upload_to_mongodb(self, file, payload):
        """
            Uploads a video to MongoDB GridFS and sends a message to RabbitMQ.

            Args:
                file: Video file to upload.
                payload (dict): Payload containing username.

            Returns:
                tuple: A tuple containing the result and HTTP status code.
        """
        try:
            # Upload the file to MongoDB GridFS
            video_file_id = self.mongo_gridfs.put(file)
        except Exception as error:
            # Return internal server error if upload fails
            return "internal server error", 500

        # Create a message to send to RabbitMQ
        message = {
            "video_file_id": str(video_file_id),
            "mp3_file_id": None,
            "username": payload["username"],
        }

        try:
            # Send the message to RabbitMQ
            self.rabbitmq_channel.basic_publish(
                exchange="",
                routing_key=os.environ.get("VIDEO_QUEUE"),
                body=json.dumps(message),
                property=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
            )
        except:
            # Delete the uploaded file if message sending fails
            self.mongo_gridfs.delete(video_file_id)
            return "internal server error", 500
