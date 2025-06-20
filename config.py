import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

class Config:
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'dev')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL', 'localhost:9092')
    KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'user_interactions')
    METADATA_ENDPOINT = os.environ.get('METADATA_ENDPOINT', 'http://localhost:8585/api')
    METADATA_JWT_TOKEN = os.environ.get('METADATA_JWT_TOKEN', '')
    MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost:27017')
    MONGO_USER = os.environ.get('MONGO_USER', '')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', '')

