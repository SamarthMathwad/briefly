import sys
import os
import json
import ssl
import urllib.request
import pdfplumber

# --- PART 1: THE EYES (Robust PDF Extraction) ---
def analyze_document_robust(pdf_path):
    print(f"👁️ Scanning: {os.path.basename(pdf_path)}...")
    full_content = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_num = i + 1
                text = page.extract_text() or ""
                
                # Check for visual elements (Graphs/Charts)
                num_visuals = len(page.images) + len(page.rects) + len(page.lines)
                
                visual_note = ""
                if num_visuals > 5:
                    visual_note = f"[NOTE: Page {page_num} contains significant VISUAL DATA.]"

                if not text.strip() and num_visuals > 0:
                    text = "[SCANNED PAGE DETECTED - Text unavailable without OCR]"
                elif not text.strip():
                    text = "[BLANK PAGE]"

                page_content = f"--- PAGE {page_num} ---\n{visual_note}\n{text}\n"
                full_content.append(page_content)
                
        return "\n".join(full_content)
    except Exception as e:
        print(f"❌ PDF Error: {e}")
        sys.exit(1)

# --- PART 2: THE BRAIN (Self-Healing Connection) ---
def generate_summary_native(text, api_key):
    print("🧠 AI Processing (Direct Connection)...")
    
    # LIST OF MODELS TO TRY (If one fails, we try the next)
    models = [
        "gemini-1.5-flash", 
        "gemini-pro", 
        "gemini-1.5-pro-latest",
        "gemini-1.0-pro"
    ]
    
    # SSL Context to BYPASS network blocks
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    prompt = f"""
    You are a high-level analyst.
    Rules:
    1. Look for "[NOTE: ... VISUAL DATA ...]". If found, start with: "**Visuals Detected:** Document contains graphs regarding [Topic]."
    2. Summarize content in 5 bullet points.
    3. No fluff.

    DOCUMENT TEXT:
    {text}
    """

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    last_error = ""

    # LOOP THROUGH MODELS UNTIL ONE WORKS
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
                result = json.loads(response.read().decode('utf-8'))
                # If we get here, it worked!
                print(f"   ✅ Success with {model_name}!")
                return result['candidates'][0]['content']['parts'][0]['text']

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            # If 404 (Not Found), we just try the next model
            if e.code == 404:
                print(f"   ⚠️ {model_name} not found. Switching...")
                last_error = f"{model_name}: 404 Not Found"
                continue
            else:
                return f"❌ HTTP Error {e.code}: {error_body}"
        except Exception as e:
            return f"❌ Network Error: {e}"

    return f"❌ All models failed. Last error: {last_error}"

# --- PART 3: EXECUTION ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/run_everything.py <file_path>")
        sys.exit(1)
        
    input_path = sys.argv[1].strip('"').strip("'")
    
    if not os.path.exists(input_path):
        print("❌ File not found.")
        sys.exit(1)

    print("-" * 40)
    api_key = input("🔑 Paste API Key: ").strip()
    print("-" * 40)

    clean_text = analyze_document_robust(input_path)
    summary = generate_summary_native(clean_text, api_key)

    print("\n" + "="*40)
    print("      RUTHLESS SUMMARY")
    print("="*40)
    print(summary)
    print("="*40 + "\n")