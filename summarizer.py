import spacy
from heapq import nlargest 
import math

nlp = spacy.load('en_core_web_sm')

def summarize_text(text, percentage = 0.4):
    doc = nlp(text)
    keywords = []
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        if token.pos_ in ['NOUN', 'VERB', 'ADJ', 'PROPN']:
            keywords.append(token.text)

    freq_word={}
    for word in keywords:
        freq_word[word] = freq_word.get(word, 0)+1
    max_freq=max(freq_word.values())
    for word in freq_word.keys():
        freq_word[word] = freq_word[word]/max_freq
        
    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                sent_strength[sent] = sent_strength.get(sent, 0)+ freq_word[word.text]

                    
    select_length = int(len(list(doc.sents)) * percentage)
    summary_sentences = nlargest(select_length, sent_strength, key=sent_strength.get)
    final_summary = [word.text for word in summary_sentences]
    
    # --- ADD THESE 2 LINES ---
    # Pick top 5 important words
    top_keywords = nlargest(5, freq_word, key=freq_word.get) 
    
    # Return BOTH values
    return " ".join(final_summary), top_keywords

# Add this function inside summarizer.py
def extract_entities(text):
    doc = nlp(text)
    entities = []
    # We only care about these specific types for professional use
    target_labels = ["ORG", "PERSON", "GPE", "DATE", "MONEY"]
    
    for ent in doc.ents:
        if ent.label_ in target_labels:
            entities.append((ent.text, ent.label_))
            
    # Return unique entities to avoid duplicates
    return list(set(entities))


# --- TESTING BLOCK ---
if __name__ == "__main__":
    # 1. Fake Text with Names and Places
    sample_text = """
    SpaceX is a private aerospace company founded by Elon Musk in 2002.
    Headquartered in California, it has revolutionized space travel.
    NASA awarded SpaceX a $2.9 billion contract to land astronauts on the Moon.
    """
    
    print("--- 1. TESTING SUMMARIZER ---")
    summary, keywords = summarise_text(sample_text)
    print(f"Summary: {summary}")
    print(f"Keywords: {keywords}")
    
    print("\n--- 2. TESTING ENTITY EXTRACTION ---")
    entities = extract_entities(sample_text)
    print(f"Found Entities: {entities}")