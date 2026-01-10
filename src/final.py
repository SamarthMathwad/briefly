import sys
import os
import json
import ssl
import urllib.request
import pdfplumber

def analyze_document_robust(pdf_path):
    print(f"👁️ Scanning: {os.path.basename(pdf_path)}...")
    full_content = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                num_visuals = len(page.images) + len(page.rects) + len(page.lines)
                
                visual_note = ""
                if num_visuals > 5:
                    visual_note = f"[NOTE: Page {i+1} contains significant VISUAL DATA.]"

                if not text.strip() and num_visuals > 0:
                    text = "[SCANNED PAGE DETECTED]"
                elif not text.strip():
                    text = "[BLANK PAGE]"

                full_content.append(f"--- PAGE {i+1} ---\n{visual_note}\n{text}\n")
        return "\n".join(full_content)
    except Exception as e:
        print(f"❌ PDF Error: {e}")
        sys.exit(1)

def generate_summary_native(text, api_key):
    print("🧠 AI Processing (Direct Connection)...")
    
    # Try these models one by one
    models = ["gemini-1.5-flash", "gemini-pro", "gemini-1.0-pro"]
    
    # Network Bypass settings
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    prompt = f"Summarize this document in 5 bullet points. Be ruthless and concise:\n\n{text}"
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    for model_name in models:
        print(f"   Trying model: {model_name}...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        
        try:
            req = urllib.request.Request(
                url, 
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))['candidates'][0]['content']['parts'][0]['text']

        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"   ⚠️ {model_name} not found. Switching...")
                continue
            return f"❌ HTTP Error {e.code}"
        except Exception as e:
            return f"❌ Network Error: {e}"

    return "❌ All models failed. Your API Key is likely broken."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python final.py <file_path>")
        sys.exit(1)
        
    input_path = sys.argv[1].strip('"').strip("'")
    if not os.path.exists(input_path):
        print("❌ File not found.")
        sys.exit(1)

    print("-" * 40)
    api_key = input("🔑 Paste NEW API Key: ").strip()
    print("-" * 40)

    clean_text = analyze_document_robust(input_path)
    print("\n" + "="*40 + "\n      SUMMARY\n" + "="*40)
    print(generate_summary_native(clean_text, api_key))