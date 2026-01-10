import google.generativeai as genai

# Paste your key here inside the quotes
GOOGLE_API_KEY = "AIzaSyD-GtO9g-rByrdt2b9uv-a-I68NshwiKvs"

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("If you can read this, the API key is working perfectly.")
    print("\n✅ SUCCESS! The key works.")
    print("Response from Gemini:", response.text)
except Exception as e:
    print("\n❌ FAILURE. The key or account is the issue.")
    print("Error details:", e)