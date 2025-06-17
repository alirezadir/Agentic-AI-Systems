import re
import logging
from typing import Literal

def classify_intent(query: str) -> Literal["pricing", "troubleshooting", "general"]:
    if re.search(r"price|cost|fee", query, re.IGNORECASE):
        return "pricing"
    elif re.search(r"error|issue|problem|fail", query, re.IGNORECASE):
        return "troubleshooting"
    else:
        return "general"

def route_to_model(intent: str) -> str:
    model_map = {
        "pricing": "gpt-4",
        "troubleshooting": "gpt-3.5-turbo",
        "general": "gpt-3.5-turbo"
    }
    chosen_model = model_map.get(intent, "gpt-3.5-turbo")
    logging.info(f"Routing intent '{intent}' to model '{chosen_model}'")
    return chosen_model
