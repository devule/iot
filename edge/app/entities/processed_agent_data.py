from pydantic import BaseModel, field_validator
from app.entities.agent_data import AgentData
from datetime import datetime


class ProcessedAgentData(BaseModel):
    road_state: str
    agent_data: AgentData
    user_id: int
    timestamp: datetime

    @classmethod
    @field_validator("timestamp", mode="before")
    def parse_timestamp(cls, value):
        # Convert the timestamp to a datetime object
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError(
                "Invalid timestamp format. Expected ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)."
            )
