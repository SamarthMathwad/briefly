# NEW WORKING CODE
import sys
import os

# 1. Import your PDF tools (Keep using your existing code!)
from src import pdf_processor, preprocess 

# 2. Import the new Local Summarizer we just made
# (We add the parent folder to path so we can find summarizer.py)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from summarizer import summarize_text

def run_docaction(pdf_path):
    print(f"Processing {pdf_path}...")
    
    # Step A: Use your EXISTING src files to get text
    raw_text = pdf_processor.extract_text(pdf_path)
    clean_text = preprocess.clean(raw_text) # If you have a clean function
    
    # Step B: Feed it to the new Engine
    print("Summarizing...")
    summary = summarize_text(clean_text, percentage=0.3)
    
    return summary