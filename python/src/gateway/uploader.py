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

import pika, json


def upload_video_to_mongodb(file, mongo_gridfs, rabbitmq_channel, payload):
    """
    - Upload the file to mongodb gridfs
    - Put a message on the queue
    """
    try:
        video_file_id = mongo_gridfs.put(file)
    except Exception as error:
        return "internal server error", 500

    message = {
        "video_file_id": str(video_file_id),
        "mp3_file_id": None,
        "username": payload["username"],
    }

    try:
        rabbitmq_channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            property=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except:
        mongo_gridfs.delete(video_file_id)
        return "internal server error", 500
