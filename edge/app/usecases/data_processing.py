from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData
from datetime import datetime


def process_agent_data(
    agent_data: AgentData,
    user_id: int,
    timestamp: datetime,
) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.
    Parameters:
        agent_data (AgentData): Agent data that containing accelerometer, GPS, and timestamp.
    Returns:
        processed_data_batch (ProcessedAgentData): Processed data containing the classified state of the road surface and agent data.
    """
    road_surface_state = "ok" if agent_data.accelerometer.x > 0 else "bumpy"

    return ProcessedAgentData(
        road_state=road_surface_state,
        agent_data=agent_data,
        user_id=user_id,
        timestamp=timestamp,
    )
