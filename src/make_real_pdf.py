# src/make_real_pdf.py
import fitz  # PyMuPDF
import os

# Define realistic invoice text
# We use '$' because your regex supports it well
text_content = """
INVOICE #2024-001
Date: 29 Dec 2025
------------------------------------------------
To: TechCorp Solutions
From: Rahul Sharma (Developer)

Description:
1. Python Backend Development ...... $1,500
2. AI Model Integration ............ $2,000
3. Server Maintenance .............. $350

TOTAL AMOUNT DUE: $3,850

Payment Instructions:
Please transfer the total amount by 10 Jan 2026.
Send confirmation to rahul@example.com once paid.
------------------------------------------------
Thank you for your business!
"""

# Setup path to save in 'examples' folder
base_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(base_dir, "..", "examples", "invoice.pdf")

# Create the PDF
doc = fitz.open()
page = doc.new_page()

# Write text with some basic formatting
# (x, y) coordinates determine where text appears
page.insert_text((50, 50), "INVOICE", fontsize=20, fontname="helv", color=(0, 0, 1)) # Blue Title
page.insert_text((50, 100), text_content, fontsize=12, fontname="cour") # Monospace font for data

doc.save(save_path)

print(f"✅ Professional PDF created at: {save_path}")