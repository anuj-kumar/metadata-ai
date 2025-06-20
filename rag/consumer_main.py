import os
from rag.consumer import OpenMetadataKafkaConsumer
from dotenv import load_dotenv

load_dotenv()

def main():
    kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    kafka_topic = os.getenv("KAFKA_TOPIC", "openmetadata.assets")
    mongo_user = os.getenv("MONGO_USER", "root")
    mongo_password = os.getenv("MONGO_PASSWORD", "example")
    collection_name = os.getenv("MONGO_COLLECTION", "assets")

    consumer = OpenMetadataKafkaConsumer(
        kafka_bootstrap_servers=kafka_bootstrap_servers,
        kafka_topic=kafka_topic,
        mongo_user=mongo_user,
        mongo_password=mongo_password,
        collection_name=collection_name,
    )
    print(f"Listening to Kafka topic '{kafka_topic}' on '{kafka_bootstrap_servers}'...")
    consumer.run()

if __name__ == "__main__":
    main()

