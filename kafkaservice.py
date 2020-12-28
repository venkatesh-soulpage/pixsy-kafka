import json
from app import db
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import uuid
from models import Match, Photo, Prediction
from sqlalchemy.exc import IntegrityError


BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC_NAME = "vectors"


""" Kafka endpoints """


# @socketio.on("kafkaconsumer", namespace="/kafka")
def kafkaconsumer():
    consumer = KafkaConsumer(bootstrap_servers=BOOTSTRAP_SERVERS)

    tp = TopicPartition(TOPIC_NAME, 0)
    # register to the topic
    consumer.assign([tp])

    # obtain the last offset value
    consumer.seek_to_end(tp)
    lastOffset = consumer.position(tp)
    consumer.seek_to_beginning(tp)

    for message in consumer:
        # print(message, "msg", message.offset, lastOffset)
        consumer_message = message
        message = json.loads(message.value)

        if message.get("type") == "photos":
            model_data = [
                Photo(name=data.get("name"), data=data.get("data"))
                for data in message.get("data")
            ]
        elif message.get("type") == "matches":
            model_data = [
                Match(name=data.get("name"), data=data.get("data"))
                for data in message.get("data")
            ]
        elif message.get("type") == "prediction":
            model_data = [
                Prediction(
                    photo=data.get("photo"),
                    match=data.get("match"),
                    status=data.get("status"),
                    score=data.get("score"),
                )
                for data in message.get("data")
            ]

        try:
            db.session.add_all(model_data)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

        if consumer_message.offset == lastOffset - 1:
            break

    consumer.close()


# @socketio.on("kafkaproducer", namespace="/kafka")
def kafkaproducer(message, im_type):
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    message_id = str(uuid.uuid4())
    message = {
        "request_id": message_id,
        "data": message,
        "type": im_type,
    }

    producer.send(TOPIC_NAME, json.dumps(message).encode("utf-8"))
    producer.flush()

    kafkaconsumer()
    producer.close()
