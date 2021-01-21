#! /usr/bin/env python
# -*- coding: utf-8 -*-

# https://www.cnblogs.com/qingyunzong/p/9004509.html
# https://www.cnblogs.com/sanduzxcvbnm/p/11579199.html

import json
from kafka import KafkaConsumer


class Config:
    KAFKA_HOST = "127.0.0.1"
    KAFKA_PORT = "1234"
    KAFKA_TOPIC = "data_topic"


def get_data_from_kafka():
    kafka_address = [f"{Config.KAFKA_HOST}:{Config.KAFKA_PORT}"]
    topic = Config.KAFKA_TOPIC

    consumer = KafkaConsumer(topic, bootstrap_servers=kafka_address, auto_offset_reset='earliest',
                             consumer_timeout_ms=1000)

    consumer.poll(timeout_ms=500)

    for msg in consumer:
        data = json.loads(msg.value.decode("utf-8"))
