from pydantic import BaseModel, Field
from typing import Dict, Any
from utils.kafka_producer import produce_to_kafka
from config import Config

class FeedbackSignal(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    signal_type: str = Field(..., description="Type of feedback or signal (e.g., 'like', 'dislike', 'correction', etc.)")
    signal_value: str = Field(..., description="Value or content of the signal (e.g., 'positive', 'negative', 'fix suggested', etc.)")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context for the feedback (e.g., query, tool, timestamp, etc.)")

def track_interaction(feedback: FeedbackSignal):
    broker = getattr(Config, 'KAFKA_BROKER_URL', 'localhost:9092')
    topic = getattr(Config, 'KAFKA_TOPIC', 'user_interactions')
    produce_to_kafka(broker, topic, feedback.model_dump())
