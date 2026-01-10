# src/rules.py

import re
from typing import List, Dict

# Regex for amounts
AMOUNT_PATTERN = re.compile(r"(₹\s?\d{1,3}(?:,\d{3})*|\$\s?\d+(?:,\d{3})*)")

# Regex for simple dates (DD/MM/YYYY, DD MMM, etc.)
DATE_PATTERN = re.compile(r"(\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?|\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))")

def extract_amounts(text: str, sentence_index: int = 0, start_offset: int = 0) -> List[Dict]:
    results = []
    for match in AMOUNT_PATTERN.finditer(text):
        results.append({
            "value": match.group(),
            "start": start_offset + match.start(),
            "end": start_offset + match.end(),
            "sentence_index": sentence_index,
            "method": "regex"
        })
    return results

def extract_dates(text: str, sentence_index: int = 0, start_offset: int = 0) -> List[Dict]:
    results = []
    for match in DATE_PATTERN.finditer(text):
        results.append({
            "value": match.group(),
            "start": start_offset + match.start(),
            "end": start_offset + match.end(),
            "sentence_index": sentence_index,
            "method": "regex"
        })
    return results
