import json
from kafka import KafkaConsumer
from rag.embedder import LangchainEmbedder
from rag.vector_store import MongoVectorStore
from mongo import get_collection

class OpenMetadataKafkaConsumer:
    def __init__(self, kafka_bootstrap_servers, kafka_topic, mongo_user, mongo_password, collection_name):
        self.consumer = KafkaConsumer(
            kafka_topic,
            bootstrap_servers=kafka_bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        self.embedder = LangchainEmbedder()
        collection = get_collection(mongo_user, mongo_password, collection_name)
        self.vector_store = MongoVectorStore(collection)

    def process_message(self, message):
        # Assume message contains 'asset_id' and 'text' fields
        asset_id = message['asset_id']
        text = message['text']
        metadata = message.get('metadata', {})
        embedding = self.embedder.embed([text])[0]
        # Fix: ensure embedding is a list, not a numpy array
        if hasattr(embedding, 'tolist'):
            embedding = embedding.tolist()
        self.vector_store.update(asset_id, embedding, metadata)

    def run(self):
        for msg in self.consumer:
            self.process_message(msg.value)
