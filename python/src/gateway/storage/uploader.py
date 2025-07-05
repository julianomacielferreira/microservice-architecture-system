import pika, json


def upload_video_to_mongodb(file, mongoGridFS, rabbitMQChannel, payload):
    """
    - Upload the file to mongodb gridfs
    - Put a message on the queue
    """
    try:
        video_fileID = mongoGridFS.put(file)
    except Exception as error:
        return "internal server error", 500

    message = {
        "video_fileID": str(video_fileID),
        "mp3_fileID": None,
        "username": payload["username"],
    }

    try:
        rabbitMQChannel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            property=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except:
        mongoGridFS.delete(video_fileID)
        return "internal server error", 500
