# src/segment.py

import re
from typing import List, Dict

# Simple sentence-ending regex
SENTENCE_END = re.compile(r'([.!?])')

def segment_sentences(text: str) -> List[Dict]:
    """
    Splits text into sentences while preserving start and end positions.
    Returns a list of dicts with:
        - 'text': sentence text
        - 'start': start index in original text
        - 'end': end index in original text
    """
    sentences = []
    start = 0

    for match in SENTENCE_END.finditer(text):
        end = match.end()
        sentence_text = text[start:end].strip()

        if sentence_text:
            sentences.append({
                "text": sentence_text,
                "start": start,
                "end": end
            })

        start = end

    # Capture any leftover text
    if start < len(text):
        tail = text[start:].strip()
        if tail:
            sentences.append({
                "text": tail,
                "start": start,
                "end": len(text)
            })

    return sentences
