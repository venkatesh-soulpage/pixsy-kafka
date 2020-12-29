import json
import os
from app import db
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import uuid
from models import Match, Photo, Prediction
from sqlalchemy.exc import IntegrityError
import dask.dataframe as dd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import RobustScaler
from sklearn import metrics
import pickle
import pandas as pd
from datetime import datetime


BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC_NAME = "vectors"


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

        if consumer_message.offset == lastOffset - 1:
            break

    consumer.close()


def kafkaproducer(message):
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    message_id = str(uuid.uuid4())
    message = {
        "request_id": message_id,
        "data": message,
    }

    producer.send(TOPIC_NAME, json.dumps(message).encode("utf-8"))
    producer.flush()
    producer.close()


sample_data = pd.read_csv("pixsy_duplicate.csv")
sample_data = sample_data.loc[:, ~sample_data.columns.str.contains("^Unnamed")]
sample_data.set_index("imageId", inplace=True)

json_data = json.loads(sample_data.to_json(orient="table"))
imageId_list = list(map(lambda d: d.pop("imageId"), json_data["data"]))
data = json_data["data"]
producer_data = []
start = datetime.now().time()
print("producer started", start)
for index in range(len(imageId_list)):
    kafkaproducer({"name": imageId_list[index], "data": data[index]})
print("producers completed", datetime.now().time())
kafkaconsumer()
print("start time", start)
print("end time", datetime.now().time())
