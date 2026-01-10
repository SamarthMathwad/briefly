import google.generativeai as genai
import pdfplumber

# --- PASTE YOUR API KEY HERE DIRECTLY (Simple & Fast) ---
# Go to aistudio.google.com to get a key if you lost it.
MY_API_KEY = "PASTE_YOUR_GEMINI_API_KEY_HERE" 

genai.configure(api_key=MY_API_KEY)

def analyze_pdf(pdf_path):
    print(f"   ...Reading {pdf_path}...")
    
    # 1. Read the PDF (The "Eyes")
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                full_text += page.extract_text() or ""
    except Exception as e:
        return f"Error reading PDF: {e}"

    # 2. Send to AI (The "Brain") - FIXED MODEL NAME
    print("   ...Sending to AI brain (Gemini 1.5)...")
    try:
        # We use 'gemini-1.5-flash' -> It is faster and DOES NOT give 404 errors.
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Summarize this document in 3 bullet points:\n{full_text[:5000]}"
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Connection Error: {e}"