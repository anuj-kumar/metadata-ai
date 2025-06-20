from kafka import KafkaProducer
import json

def produce_to_kafka(broker, topic, data):
    producer = KafkaProducer(
        bootstrap_servers=[broker],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    producer.send(topic, data)
    producer.flush()

