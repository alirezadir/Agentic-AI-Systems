import re
import logging
from typing import Optional

EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PHONE_REGEX = re.compile(r'\b\d{10,}\b')
CREDIT_CARD_REGEX = re.compile(r'\b(?:\d[ -]*?){13,16}\b')
TOXIC_WORDS = {"idiot", "hate", "stupid"}

def sanitize_input(text: str) -> str:
    text = EMAIL_REGEX.sub('[REDACTED_EMAIL]', text)
    text = PHONE_REGEX.sub('[REDACTED_PHONE]', text)
    text = CREDIT_CARD_REGEX.sub('[REDACTED_CREDIT_CARD]', text)
    return text

def detect_toxic_input(text: str) -> Optional[str]:
    for word in TOXIC_WORDS:
        if word in text.lower():
            return f"Toxic content detected: '{word}'"
    return None

def validate_input(text: str) -> bool:
    sanitized = sanitize_input(text)
    issue = detect_toxic_input(sanitized)
    if issue:
        logging.warning(issue)
        return False
    return True

def validate_output(text: str) -> str:
    if not text.strip():
        return "[Error] Output was empty."
    if any(w in text.lower() for w in TOXIC_WORDS):
        return "[Warning] The output contains inappropriate content."
    if "as an AI language model" in text.lower():
        return text.replace("As an AI language model,", "").strip()
    return text
