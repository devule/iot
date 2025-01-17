import json
import logging
from typing import List

import pydantic_core
import requests
from datetime import datetime

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (dict): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        url = f"{self.api_base_url}/processed_agent_data/"
        response = requests.post(url, json=json.loads(json.dumps([item.model_dump() for item in processed_agent_data_batch], cls=DateTimeEncoder)))
        if response.status_code == 200:
            return True
        return False
