# src/ner.py

import spacy

# Load English model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str):
    doc = nlp(text)
    results = []
    for ent in doc.ents:
        results.append({
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char
        })
    return results

if __name__ == "__main__":
    sample_text = "Pay Rahul ₹5,000 by 12 Aug. ₹2,000 for groceries."
    ents = extract_entities(sample_text)
    print(ents)
