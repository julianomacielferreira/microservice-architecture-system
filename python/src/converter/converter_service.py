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

import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy


class VideoToMp3Converter:
    """
        Class responsible for converting videos to MP3 and sending a message to RabbitMQ.
    """

    def __init__(self, fs_videos, fs_mp3s, rabbitmq_channel):
        """
            Initializes the class with MongoDB GridFS instances and RabbitMQ channel.

            Args:
                fs_videos: MongoDB GridFS instance for videos.
                fs_mp3s: MongoDB GridFS instance for MP3s.
                rabbitmq_channel: RabbitMQ channel instance.
        """
        self.fs_videos = fs_videos
        self.fs_mp3s = fs_mp3s
        self.rabbitmq_channel = rabbitmq_channel

    def write_video_content_to_temp_file(self, message):
        """
            Writes video content to a temporary file.

            Args:
              message (dict): Message containing video file ID.

            Returns:
             TemporaryFile: Temporary file containing video content.
        """
        temporary_file = tempfile.TemporaryFile()

        out = self.fs_videos.get(ObjectId(message['video_fileID']))

        temporary_file.write(out.read())

        return temporary_file

    def convert_to_mp3(self, message):
        """
           Converts a video to MP3 and sends a message to RabbitMQ.

           Args:
            message (str): JSON string message containing video file ID.

           Returns:
            str: Result of the conversion process.
        """

        # Convert the JSON string message to a Python object
        message = json.loads(message)

        # Create a temporary file
        temporary_file = self.write_video_content_to_temp_file(message)

        # Convert video file to audio file
        audio = moviepy.VideoFileClip(temporary_file.name).audio

        temporary_file.close()

        # Write file to its own file
        temporary_file_path = tempfile.gettempdir() + f"/{message['video_file_id']}.mp3"

        audio.write_audiofile(temporary_file_path)

        # Open file in read mode
        file = open(temporary_file_path, "rb")

        # Read the data from the file
        data = file.read()

        # Save data in MongoDB
        mp3_file_id = self.fs_mp3s.put(data)

        # Close file
        file.close()

        # Remove temporary file
        os.remove(temporary_file_path)

        # Put the new message in the queue
        message["mp3_file_id"] = str(mp3_file_id)

        try:
            self.rabbitmq_channel.basic_publish(
                exchange="",
                routing_key=os.environ.get("MP3_QUEUE"),
                body=json.dumps(message),
                property=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                )
            )
        except Exception as err:
            self.fs_mp3s.delete(mp3_file_id)
            return "failed to publish message"

        return "success"
