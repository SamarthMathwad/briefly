# src/make_pdf.py
import fitz
import os

text_content = """
INVOICE #1024
----------------
Please transfer $8,500 to Priya by 15 Sept.
Also pay $1,200 for the electricity bill.
"""

base_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(base_dir, "..", "examples", "sample.pdf")

doc = fitz.open()
page = doc.new_page()
page.insert_text((50, 50), text_content, fontsize=12)
doc.save(save_path)

print(f"✅ PDF created successfully at: {save_path}")