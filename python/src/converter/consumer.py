import pika, sys, os, time
from pymongo import MongoClient
import gridfs
from mp3_converter import video_to_mp3

"""
    Consumer service that pulls the messages off rabbitmp queue
    to konw which videos have to convert and to store, etc.
"""


def main():
    client = MongoClient("host.minikube.internal", 27017)
    db_videos = client.videos
    db_mp3s = client.mp3s

    # gridfs
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    # rabbitmq connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    rabbitMQChannel = connection.channel()

    VIDEO_QUEUE = os.environ.get("VIDEO_QUEUE")

    """
        Whenever a message is taken off the queue by this consumer service
        this callback function is called 
    """

    def callback(channel, method, properties, body):
        err = video_to_mp3.start(body, fs_videos, fs_mp3s, channel)

        # if there is an error, send a negative acknowledgment to keep message on the queue
        if err:
            channel.basic_nack(delivery_tag=method.delivery_tag)
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)

    rabbitMQChannel.basic_consume(queue=VIDEO_QUEUE, on_message_callback=callback)

    print("Waiting for the messages. To exit press CTRL C")

    rabbitMQChannel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
