from google import genai
import os

print("-" * 30)
key = input("🔑 Paste your API Key here and hit Enter: ").strip()
print("-" * 30)

try:
    client = genai.Client(api_key=key)
    print("\n🔍 Scanning for available models...")
    
    found = False
    for m in client.models.list():
        if "generateContent" in m.supported_generation_methods:
            # Strip the 'models/' prefix to get the clean name
            clean_name = m.name.replace("models/", "")
            print(f"✅ FOUND: {clean_name}")
            found = True
            
    if not found:
        print("❌ No text-generation models found. Check your API permissions.")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("Double check that you pasted the full key correctly!")