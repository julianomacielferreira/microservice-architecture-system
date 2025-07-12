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


def write_video_content_to_temp_file(fs_videos, message):
    # create an empty temporary file
    temporary_file = tempfile.TemporaryFile()

    # video contents
    out = fs_videos.get(ObjectId(message['video_fileID']))

    # add video contents to tempFile
    temporary_file.write(out.read())

    return temporary_file


def convert_video_to_mp3(message, fs_videos, fs_mp3s, rabbitmq_channel):
    # Convert the json string message to a python object
    message = json.loads(message)

    # create a temporary file
    temporary_file = write_video_content_to_temp_file(fs_videos, message)

    # convert video file to audio file
    audio = moviepy.VideoFileClip(temporary_file.name).audio

    temporary_file.close()

    # write file to its own file
    temporary_file_path = tempfile.gettempdir() + f"/{message['video_file_id']}.mp3"

    audio.write_audiofile(temporary_file_path)

    # open file in read mode
    file = open(temporary_file_path, "rb")

    # read the data from the file
    data = file.read()

    # save data in mongoDB
    mp3_file_id = fs_mp3s.put(data)

    # close file
    file.close()

    # remove temporary file
    os.remove(temporary_file_path)

    # put the new message in the queue
    message["mp3_file_id"] = str(mp3_file_id)

    try:
        rabbitmq_channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            property=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        fs_mp3s.delete(mp3_file_id)
        return "failed to publish message"
