# coding=utf-8
# Date ：2019/12/23 14:20
__author__ = 'Maojun'

from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka import KafkaClient, SimpleClient
import time
import os
"""pip install kafka-python
https://zhuanlan.zhihu.com/p/38330574"""

client = SimpleClient(hosts="10.245.251.175:9092")
print(client.topics)


consumer = KafkaConsumer('my_topic', bootstrap_servers=['10.245.251.175:9092'], auto_offset_reset='latest')
print(consumer.topics())
print(consumer.assignment())
print(consumer.subscription())


"""PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL"""
producer = KafkaProducer(security_protocol='PLAINTEXT',
                         bootstrap_servers=os.environ.get('admin', '10.245.251.175:9092'))
print(producer.bootstrap_connected())

